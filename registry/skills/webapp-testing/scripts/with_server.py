#!/usr/bin/env python3
"""Run a command while one or more servers are started and monitored."""

from __future__ import annotations

import argparse
import json
import subprocess
import socket
import sys
import time


def is_server_ready(port: int, timeout: int = 30) -> bool:
    """Wait until a TCP port starts accepting connections."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def parse_server_command(raw: str, allow_shell: bool) -> str | list[str]:
    if allow_shell:
        return raw

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("server command must be JSON unless --allow-shell is set") from exc

    if not isinstance(payload, list) or not payload:
        raise ValueError("server command JSON must be a non-empty string array")
    if any(not isinstance(item, str) or not item for item in payload):
        raise ValueError("server command JSON must contain only non-empty strings")
    return payload


def describe_command(command: str | list[str]) -> str:
    if isinstance(command, str):
        return command
    return " ".join(command)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run command with one or more servers")
    parser.add_argument("--server", action="append", dest="servers", required=True, help="Server command (repeatable)")
    parser.add_argument("--port", action="append", dest="ports", type=int, required=True, help="Port per server")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds per server")
    parser.add_argument("--allow-shell", action="store_true", help="Allow raw shell strings for server commands")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to run after server(s) are ready")

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
    for raw_command, port in zip(args.servers, args.ports):
        servers.append({"cmd": parse_server_command(raw_command, args.allow_shell), "port": port})

    server_processes = []

    try:
        for i, server in enumerate(servers):
            print(f"Starting server {i+1}/{len(servers)}: {describe_command(server['cmd'])}")
            process = subprocess.Popen(
                server["cmd"],
                shell=isinstance(server["cmd"], str),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
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
