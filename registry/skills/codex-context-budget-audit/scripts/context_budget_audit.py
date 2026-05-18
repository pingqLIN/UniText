#!/usr/bin/env python3
"""Estimate locally observable Codex initial-context budget sources."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]


TOKEN_LOW_CHARS = 4.0
TOKEN_HIGH_CHARS = 3.0

ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "gray": "\033[90m",
}

HTML_COLORS = {
    "bold": "#e5e7eb",
    "cyan": "#22d3ee",
    "green": "#22c55e",
    "yellow": "#facc15",
    "blue": "#60a5fa",
    "magenta": "#c084fc",
    "gray": "#9ca3af",
    "white": "#e5e7eb",
}


@dataclass
class Phase:
    name: str
    status: str
    count: int = 0
    chars: int = 0
    tokens_low: int = 0
    tokens_high: int = 0
    note: str = ""


def estimate_tokens(chars: int) -> tuple[int, int]:
    return round(chars / TOKEN_LOW_CHARS), round(chars / TOKEN_HIGH_CHARS)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""


def load_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    if tomllib is None:
        raise RuntimeError("Python 3.11+ tomllib is required to parse TOML")
    with path.open("rb") as handle:
        return tomllib.load(handle)


def description_from_skill(path: Path) -> str:
    text = read_text(path)
    match = re.search(r"^description:\s*(.*)$", text, re.MULTILINE)
    if not match:
        return ""
    desc = match.group(1).strip().strip("'\"")
    return re.sub(r"\s+", " ", desc)[:48]


def skill_manifest_phase(name: str, root: Path, label: str) -> Phase:
    files = sorted(root.glob("*/SKILL.md")) if root.exists() else []
    lines = []
    for file in files:
        skill_name = file.parent.name
        desc = description_from_skill(file)
        lines.append(f"- {skill_name}: {desc} (file: {label}/{skill_name}/SKILL.md)")
    chars = len("\n".join(lines))
    low, high = estimate_tokens(chars)
    return Phase(name=name, status="estimated", count=len(files), chars=chars, tokens_low=low, tokens_high=high)


def full_skill_bodies_phase(name: str, root: Path) -> Phase:
    files = sorted(root.glob("*/SKILL.md")) if root.exists() else []
    chars = sum(len(read_text(file)) for file in files)
    low, high = estimate_tokens(chars)
    return Phase(
        name=name,
        status="upper-bound",
        count=len(files),
        chars=chars,
        tokens_low=low,
        tokens_high=high,
        note="full bodies are loaded only after skill trigger, not normal startup",
    )


def ancestor_agents_files(workdir: Path, codex_home: Path) -> list[Path]:
    files: list[Path] = []
    global_agents = codex_home / "AGENTS.md"
    if global_agents.exists():
        files.append(global_agents)
    current = workdir.resolve()
    parents = [current, *current.parents]
    for parent in parents:
        candidate = parent / "AGENTS.md"
        if candidate.exists() and candidate not in files:
            files.append(candidate)
        if parent.parent == parent:
            break
    return files


def text_files_phase(name: str, files: list[Path], status: str = "estimated") -> Phase:
    chars = sum(len(read_text(file)) for file in files)
    low, high = estimate_tokens(chars)
    note = "; ".join(str(file) for file in files[:5])
    if len(files) > 5:
        note += f"; +{len(files) - 5} more"
    return Phase(name=name, status=status, count=len(files), chars=chars, tokens_low=low, tokens_high=high, note=note)


def plugin_skill_files(codex_home: Path, plugin_id: str) -> list[Path]:
    if "@" not in plugin_id:
        return []
    name, marketplace = plugin_id.split("@", 1)
    roots = [
        codex_home / "plugins" / "cache" / marketplace / name,
        codex_home / ".tmp" / "marketplaces" / marketplace / "plugins" / name,
        codex_home / ".tmp" / "bundled-marketplaces" / marketplace / "plugins" / name,
    ]
    for root in roots:
        if root.exists():
            files = sorted(root.rglob("SKILL.md"))
            if files:
                return files
    return []


def plugin_manifest_phase(codex_home: Path, plugins: dict[str, Any], enabled: bool) -> Phase:
    selected = []
    for plugin_id, config in sorted(plugins.items()):
        if isinstance(config, dict) and config.get("enabled") is enabled:
            selected.append(plugin_id)
    lines = []
    count = 0
    for plugin_id in selected:
        for file in plugin_skill_files(codex_home, plugin_id):
            count += 1
            desc = description_from_skill(file)
            lines.append(f"- {file.parent.name}: {desc} (plugin: {plugin_id})")
    chars = len("\n".join(lines))
    low, high = estimate_tokens(chars)
    status = "estimated" if enabled else "disabled-cache"
    note = ", ".join(selected)
    return Phase(
        name="plugin_skill_manifest_enabled" if enabled else "plugin_skill_manifest_disabled_cache",
        status=status,
        count=count,
        chars=chars,
        tokens_low=low,
        tokens_high=high,
        note=note,
    )


def mcp_phase(mcp_servers: dict[str, Any]) -> Phase:
    real_servers = {
        name: config
        for name, config in mcp_servers.items()
        if isinstance(config, dict) and ("command" in config or "url" in config)
    }
    enabled = [name for name, config in real_servers.items() if config.get("enabled", True) is not False]
    note = "enabled: " + (", ".join(sorted(enabled)) if enabled else "none")
    return Phase(
        name="mcp_enabled_surface",
        status="count-only",
        count=len(enabled),
        chars=0,
        tokens_low=0,
        tokens_high=0,
        note=note + "; local CLI cannot see injected tool schema tokens",
    )


def config_phase(config: dict[str, Any]) -> Phase:
    features = config.get("features", {})
    plugins = config.get("plugins", {})
    mcp_servers = config.get("mcp_servers", {})
    enabled_plugins = sum(1 for value in plugins.values() if isinstance(value, dict) and value.get("enabled") is True)
    disabled_plugins = sum(1 for value in plugins.values() if isinstance(value, dict) and value.get("enabled") is False)
    real_mcp = [
        value
        for value in mcp_servers.values()
        if isinstance(value, dict) and ("command" in value or "url" in value)
    ]
    enabled_mcp = sum(1 for value in real_mcp if value.get("enabled", True) is not False)
    note = (
        f"memories={features.get('memories')}; "
        f"remote_plugin={features.get('remote_plugin')}; "
        f"plugins={enabled_plugins} enabled/{disabled_plugins} disabled; "
        f"mcp={enabled_mcp} enabled/{len(real_mcp) - enabled_mcp} disabled"
    )
    return Phase(name="config_state", status="observed", note=note)


def memory_phase(codex_home: Path, config: dict[str, Any]) -> Phase:
    enabled = config.get("features", {}).get("memories") is True
    candidates = [codex_home / "memories" / "memory_summary.md", codex_home / "memories" / "MEMORY.md"]
    files = [path for path in candidates if path.exists()]
    phase = text_files_phase("memory_summary", files[:1], "estimated" if enabled else "disabled")
    if not enabled:
        phase.tokens_low = 0
        phase.tokens_high = 0
        phase.note = "memories disabled; source size not charged in new startup estimate"
    return phase


def measured_total(phases: list[Phase]) -> tuple[int, int]:
    return sum(phase.tokens_low for phase in phases), sum(phase.tokens_high for phase in phases)


def should_use_color(mode: str) -> bool:
    if mode == "always":
        return True
    if mode == "never":
        return False
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM", "").lower() == "dumb":
        return False
    return sys.stdout.isatty()


def paint(text: str, color: str, enabled: bool) -> str:
    if not enabled:
        return text
    return f"{ANSI[color]}{text}{ANSI['reset']}"


def source_style(code: str, memory_state: str, mcp_count: int) -> str:
    if code == "SYS":
        return "yellow"
    if code == "MEM":
        return "gray" if memory_state == "off" else "green"
    if code == "DOC":
        return "blue"
    if code == "SKL":
        return "magenta"
    if code == "PLG":
        return "cyan"
    if code == "MCP":
        return "gray" if mcp_count == 0 else "yellow"
    return "white"


def source_fill(code: str, memory_state: str, mcp_count: int) -> str:
    if code == "SYS":
        return "?"
    if code == "MEM":
        return "-" if memory_state == "off" else "="
    if code == "DOC":
        return "="
    if code == "SKL":
        return "#"
    if code == "PLG":
        return "+"
    if code == "MCP":
        return "-" if mcp_count == 0 else "*"
    return "#"


def print_phase_table(phases: list[Phase]) -> None:
    print("Phased local context budget estimate")
    print("=" * 84)
    print(f"{'phase':34} {'status':14} {'count':>6} {'chars':>9} {'tokens':>15}")
    print("-" * 84)
    for phase in phases:
        token_text = f"{phase.tokens_low}-{phase.tokens_high}"
        print(f"{phase.name:34} {phase.status:14} {phase.count:6} {phase.chars:9} {token_text:>15}")
        if phase.note:
            print(f"  note: {phase.note}")
    low, high = measured_total(phases)
    print("-" * 84)
    print(f"{'measured local subtotal':34} {'estimate':14} {'':6} {'':9} {str(low) + '-' + str(high):>15}")
    print()


def bar(value: int, total: int, width: int = 28, fill: str = "#", empty: str = "-") -> str:
    if total <= 0 or value <= 0:
        filled = 0
    else:
        filled = max(1, round(width * value / total))
    return fill * filled + empty * (width - filled)


def format_token_range(low: int, high: int) -> str:
    def one(value: int) -> str:
        if value >= 1000:
            return f"{value / 1000:.1f}k"
        return str(value)

    return f"{one(low)}-{one(high)}"


def boxed_row(left: str, right: str = "", width: int = 116) -> str:
    inner = width - 4
    if right:
        available_left = inner - len(right) - 1
        left = left[:available_left]
        return f"| {left:<{available_left}} {right} |"
    return f"| {left:<{inner}} |"


def boxed_rule(width: int = 116, char: str = "-") -> str:
    return "+" + char * (width - 2) + "+"


def chart_context(phases: list[Phase]) -> tuple[list[tuple[str, str, str | None, str]], dict[str, Phase], int, int, int, str, int]:
    chart_items: list[tuple[str, str, str | None, str]] = [
        ("SYS", "platform system/developer/tools", None, "runtime-owned"),
        ("MEM", "memory summary", "memory_summary", "config-gated"),
        ("DOC", "AGENTS/workspace instructions", "agents_instructions", "local files"),
        ("SKL", "local skill manifests", "local_skill_manifest_total", "local roots"),
        ("PLG", "plugin skill manifests", "plugin_skill_manifest_enabled", "enabled plugins"),
        ("MCP", "enabled MCP tool surface", "mcp_enabled_surface", "tool schema hidden"),
    ]
    lookup = {phase.name: phase for phase in phases}
    known_values = [lookup[name].tokens_high for _, _, name, _ in chart_items if name in lookup]
    total = sum(known_values)
    low_total, high_total = measured_total(phases)
    memory_phase = lookup.get("memory_summary")
    memory_state = "off" if memory_phase and memory_phase.status == "disabled" else "on"
    mcp_phase_value = lookup.get("mcp_enabled_surface")
    mcp_count = mcp_phase_value.count if mcp_phase_value else 0
    return chart_items, lookup, total, low_total, high_total, memory_state, mcp_count


def print_ascii_chart(phases: list[Phase], use_color: bool = False) -> None:
    chart_items, lookup, total, low_total, high_total, memory_state, mcp_count = chart_context(phases)

    border = "cyan"
    print(paint("ASCII context dashboard", "bold", use_color))
    print(paint(boxed_rule(), border, use_color))
    print(paint(boxed_row("CODEX CONTEXT BUDGET", "local estimate / startup surface"), "bold", use_color))
    print(boxed_row("STYLE RAIL  | dense statusline | clear tool surface | measured-local estimate"))
    print(paint(boxed_rule(char="="), border, use_color))
    print(paint(boxed_row(f"STATUS      | LOCAL SUBTOTAL  {format_token_range(low_total, high_total)} tok", f"MEMORY {memory_state.upper()} | MCP {mcp_count} enabled"), "green" if memory_state == "off" and mcp_count == 0 else "yellow", use_color))
    print(paint(boxed_row("RUNTIME     | PLATFORM BASE   unknown", "system + developer + native tool schema"), "yellow", use_color))
    print(paint(boxed_rule(), border, use_color))
    print(paint(boxed_row("ID  | SOURCE                           | BAR                      | TOKENS       |   % | STATE"), "bold", use_color))
    print(paint(boxed_rule(), border, use_color))
    for code, label, phase_name, hint in chart_items:
        style = source_style(code, memory_state, mcp_count)
        if phase_name is None:
            line = f"{code:<3} | {label:<32} | [{'?' * 24}] | {'unknown':>12} | {'n/a':>3} | {hint:<16}"
            print(paint(boxed_row(line), style, use_color))
            continue
        phase = lookup.get(phase_name)
        if not phase:
            continue
        pct = 0 if total <= 0 else round(100 * phase.tokens_high / total)
        token_text = f"{format_token_range(phase.tokens_low, phase.tokens_high)} tok"
        bar_text = bar(phase.tokens_high, total, width=24, fill=source_fill(code, memory_state, mcp_count))
        line = f"{code:<3} | {label:<32} | [{bar_text}] | {token_text:>12} | {pct:>3}% | {hint:<16}"
        print(paint(boxed_row(line), style, use_color))
    print(paint(boxed_rule(), border, use_color))
    print(boxed_row("FLOW        | SYS ? | MEM | DOC | SKL | PLG | MCP | USER", "startup read order"))
    print(boxed_row("LIMIT       | percentages are measured-local only", "unknown SYS base kept separate"))
    print(paint(boxed_rule(), border, use_color))
    print()


def html_span(text: str, color: str, bold: bool = False) -> str:
    weight = "font-weight:700;" if bold else ""
    return f'<span style="color:{HTML_COLORS[color]};{weight}">{html.escape(text)}</span>'


def codex_bar(code: str, value: int, total: int, memory_state: str, mcp_count: int) -> str:
    fill = source_fill(code, memory_state, mcp_count)
    text = "?" * 24 if code == "SYS" else bar(value, total, width=24, fill=fill)
    style = source_style(code, memory_state, mcp_count)
    filled = text.rstrip("-")
    empty = "-" * (len(text) - len(filled))
    if not filled:
        return html_span(text, "gray")
    return html_span(filled, style, bold=code in {"SKL", "DOC"}) + html_span(empty, "gray")


def codex_dashboard_markdown(phases: list[Phase]) -> str:
    chart_items, lookup, total, low_total, high_total, memory_state, mcp_count = chart_context(phases)
    rows = []
    for code, label, phase_name, hint in chart_items:
        style = source_style(code, memory_state, mcp_count)
        if phase_name is None:
            tokens = "unknown"
            pct = "n/a"
            bar_text = html_span("?" * 24, style, bold=True)
        else:
            phase = lookup.get(phase_name)
            if not phase:
                continue
            tokens = f"{format_token_range(phase.tokens_low, phase.tokens_high)} tok"
            pct = "0%" if total <= 0 else f"{round(100 * phase.tokens_high / total)}%"
            bar_text = codex_bar(code, phase.tokens_high, total, memory_state, mcp_count)
        rows.append(
            "| "
            + " | ".join(
                [
                    html_span(code, style, bold=True),
                    html.escape(label),
                    bar_text,
                    html.escape(tokens),
                    html.escape(pct),
                    html_span(hint, style),
                ]
            )
            + " |"
        )
    header = [
        '<div style="border:1px solid #22d3ee;padding:12px 14px;border-radius:6px;background:#0b1020;color:#e5e7eb;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;">',
        f'<div style="color:#e5e7eb;font-weight:700;">CODEX CONTEXT BUDGET <span style="color:#9ca3af;font-weight:400;">local estimate / startup surface</span></div>',
        f'<div style="margin-top:6px;color:#22c55e;">STATUS | LOCAL SUBTOTAL {format_token_range(low_total, high_total)} tok | MEMORY {memory_state.upper()} | MCP {mcp_count} enabled</div>',
        '<div style="color:#facc15;">RUNTIME | PLATFORM BASE unknown | system + developer + native tool schema</div>',
        "</div>",
        "",
        "| ID | Source | Load bar | Tokens | Share | State |",
        "|---|---|---:|---:|---:|---|",
    ]
    footer = [
        "",
        '<span style="color:#9ca3af;">FLOW | SYS ? | MEM | DOC | SKL | PLG | MCP | USER</span>',
        "",
        '<span style="color:#9ca3af;">LIMIT | Percentages are measured-local only; unknown SYS base is deliberately separate.</span>',
    ]
    return "\n".join(header + rows + footer)


def print_codex_dashboard(phases: list[Phase]) -> None:
    print("Codex color dashboard")
    print(codex_dashboard_markdown(phases))
    print()


def compare_with_baseline(phases: list[Phase], baseline_path: Path) -> None:
    if not baseline_path.exists():
        print(f"Baseline not found: {baseline_path}", file=sys.stderr)
        return
    baseline = json.loads(read_text(baseline_path))
    old = {phase["name"]: phase for phase in baseline.get("phases", [])}
    print("Baseline comparison")
    print("=" * 84)
    print(f"{'phase':34} {'old_high':>10} {'new_high':>10} {'delta':>10}")
    print("-" * 84)
    for phase in phases:
        old_high = int(old.get(phase.name, {}).get("tokens_high", 0))
        delta = phase.tokens_high - old_high
        print(f"{phase.name:34} {old_high:10} {phase.tokens_high:10} {delta:10}")
    print()


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    codex_home = Path(args.codex_home).expanduser()
    workdir = Path(args.workdir).expanduser()
    config_path = Path(args.config).expanduser() if args.config else codex_home / "config.toml"
    config = load_toml(config_path)
    plugins = config.get("plugins", {})
    mcp_servers = config.get("mcp_servers", {})

    local_roots = [
        ("r0", codex_home / "skills"),
        ("r1", Path(r"Q:\UniText\runtime\skills")),
        ("r2", codex_home / "skills" / ".system"),
    ]

    phases: list[Phase] = [
        Phase("platform_prompt_base", "unobservable", note="system/developer/native tool schema are injected by runtime"),
        config_phase(config),
        memory_phase(codex_home, config),
        text_files_phase("agents_instructions", ancestor_agents_files(workdir, codex_home)),
    ]

    local_manifest_chars = 0
    local_manifest_count = 0
    for label, root in local_roots:
        phase = skill_manifest_phase(f"skill_manifest_{label}", root, label)
        phases.append(phase)
        local_manifest_chars += phase.chars
        local_manifest_count += phase.count
    low, high = estimate_tokens(local_manifest_chars)
    phases.append(
        Phase(
            name="local_skill_manifest_total",
            status="estimated",
            count=local_manifest_count,
            chars=local_manifest_chars,
            tokens_low=low,
            tokens_high=high,
        )
    )

    phases.append(plugin_manifest_phase(codex_home, plugins, True))
    phases.append(plugin_manifest_phase(codex_home, plugins, False))
    phases.append(mcp_phase(mcp_servers))

    if args.include_skill_bodies:
        for label, root in local_roots:
            phases.append(full_skill_bodies_phase(f"skill_bodies_{label}", root))

    return {
        "workdir": str(workdir),
        "codex_home": str(codex_home),
        "config": str(config_path),
        "phases": [asdict(phase) for phase in phases],
    }


def parse_args() -> argparse.Namespace:
    default_home = Path(os.environ.get("CODEX_HOME", r"C:\Users\miles\.codex"))
    parser = argparse.ArgumentParser(description="Audit locally observable Codex context/token overhead.")
    parser.add_argument("--workdir", default=os.getcwd(), help="Execution location to inspect.")
    parser.add_argument("--codex-home", default=str(default_home), help="Codex home directory.")
    parser.add_argument("--config", default=None, help="Explicit config.toml path.")
    parser.add_argument("--json-out", default=None, help="Write JSON report to this path.")
    parser.add_argument("--markdown-out", default=None, help="Write Codex-friendly colored Markdown/HTML report to this path.")
    parser.add_argument("--baseline", default=None, help="Compare against a previous JSON report.")
    parser.add_argument("--color", choices=("auto", "always", "never"), default="auto", help="ANSI color mode for terminal output.")
    parser.add_argument("--render", choices=("terminal", "codex", "both"), default="terminal", help="Dashboard renderer.")
    parser.add_argument("--include-skill-bodies", action="store_true", help="Estimate full SKILL.md bodies as upper bounds.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    use_color = should_use_color(args.color)
    phases = [Phase(**phase) for phase in report["phases"]]
    print(f"workdir: {report['workdir']}")
    print(f"codex_home: {report['codex_home']}")
    print(f"config: {report['config']}")
    print()
    print_phase_table(phases)
    if args.render in {"terminal", "both"}:
        print_ascii_chart(phases, use_color)
    if args.render in {"codex", "both"}:
        print_codex_dashboard(phases)

    if args.baseline:
        compare_with_baseline(phases, Path(args.baseline).expanduser())

    if args.json_out:
        output = Path(args.json_out).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"wrote: {output}")

    if args.markdown_out:
        output = Path(args.markdown_out).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(codex_dashboard_markdown(phases) + "\n", encoding="utf-8")
        print(f"wrote markdown: {output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
