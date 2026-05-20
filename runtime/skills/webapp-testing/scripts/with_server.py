#!/usr/bin/env python3
"""
Start one or more servers, wait for them to be ready, run a command, then clean up.

Usage:
    # Single server
    python scripts/with_server.py --server '{"cmd":["npm","run","dev"]}' --port 5173 -- python automation.py
    python scripts/with_server.py --server '{"cmd":["npm","start"]}' --port 3000 -- python test.py

    # Multiple servers with working directories
    python scripts/with_server.py \
      --server '{"cmd":["python","server.py"],"cwd":"backend"}' --port 3000 \
      --server '{"cmd":["npm","run","dev"],"cwd":"frontend"}' --port 5173 \
      -- python test.py

    # Legacy shell mode is disabled. Pass JSON server specs only.
    python scripts/with_server.py --server '{"cmd":["python","server.py"]}' --port 3000 -- python test.py
"""

import argparse
import json
import socket
import subprocess
import sys
import time
from pathlib import Path


def parse_server_spec(spec, allow_shell):
    try:
        value = json.loads(spec)
    except json.JSONDecodeError:
        raise ValueError(
            "Server spec must be JSON. "
            "Example: --server '{\"cmd\":[\"npm\",\"run\",\"dev\"],\"cwd\":\"frontend\"}'"
        )

    if allow_shell:
        raise ValueError("Legacy shell mode has been disabled; use a JSON server spec with cmd array instead")

    if not isinstance(value, dict):
        raise ValueError("Server spec JSON must be an object")

    cmd = value.get('cmd')
    cwd = value.get('cwd')
    if not isinstance(cmd, list) or not cmd or not all(isinstance(item, str) and item for item in cmd):
        raise ValueError("Server spec must include a non-empty string array in cmd")
    if cwd is not None and (not isinstance(cwd, str) or not cwd.strip()):
        raise ValueError("Server spec cwd must be a non-empty string when provided")

    return {'cmd': cmd, 'cwd': cwd}


def resolve_cwd(value):
    if value is None:
        return None
    path = Path(value)
    if path.is_absolute():
        raise ValueError("Absolute cwd is not allowed in server spec")
    if any(part == '..' for part in path.parts):
        raise ValueError("Parent traversal is not allowed in server cwd")
    return str(path)


def is_server_ready(port, timeout=30):
    """Wait for server to be ready by polling the port."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def main():
    parser = argparse.ArgumentParser(description='Run command with one or more servers')
    parser.add_argument('--server', action='append', dest='servers', required=True, help='Server command (can be repeated)')
    parser.add_argument('--port', action='append', dest='ports', type=int, required=True, help='Port for each server (must match --server count)')
    parser.add_argument('--timeout', type=int, default=30, help='Timeout in seconds per server (default: 30)')
    parser.add_argument(
        '--allow-shell',
        action='store_true',
        help='Legacy compatibility flag; shell execution is disabled for safety',
    )
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Command to run after server(s) ready')

    args = parser.parse_args()

    if args.command and args.command[0] == '--':
        args.command = args.command[1:]

    if not args.command:
        print("Error: No command specified to run")
        sys.exit(1)

    if len(args.servers) != len(args.ports):
        print("Error: Number of --server and --port arguments must match")
        sys.exit(1)

    servers = []
    for cmd, port in zip(args.servers, args.ports):
        if port < 1 or port > 65535:
            print(f"Error: Invalid port {port}")
            sys.exit(1)
        try:
            server = parse_server_spec(cmd, args.allow_shell)
            server['cwd'] = resolve_cwd(server.get('cwd'))
            server['port'] = port
            servers.append(server)
        except ValueError as exc:
            print(f"Error: {exc}")
            sys.exit(1)

    server_processes = []

    try:
        for i, server in enumerate(servers):
            print(f"Starting server {i+1}/{len(servers)}: {server['cmd']}")
            process = subprocess.Popen(
                server['cmd'],
                cwd=server['cwd'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            server_processes.append(process)

            print(f"Waiting for server on port {server['port']}...")
            if not is_server_ready(server['port'], timeout=args.timeout):
                raise RuntimeError(f"Server failed to start on port {server['port']} within {args.timeout}s")

            print(f"Server ready on port {server['port']}")

        print(f"\nAll {len(servers)} server(s) ready")
        print(f"Running: {' '.join(args.command)}\n")
        result = subprocess.run(args.command)
        sys.exit(result.returncode)

    finally:
        print(f"\nStopping {len(server_processes)} server(s)...")
        for i, process in enumerate(server_processes):
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            print(f"Server {i+1} stopped")
        print("All servers stopped")


if __name__ == '__main__':
    main()
