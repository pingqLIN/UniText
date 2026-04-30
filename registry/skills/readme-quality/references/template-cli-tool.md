# Template: CLI Tool / Python Package / Library / MCP Server

Reference project: `terminal-bridge-v2`
Characteristics: Python/Node CLI, pip/npm install, programmatic API, cross-platform

---

## Section order

```
# project-name

[繁體中文](README.zh-TW.md)

> [One-line tagline in blockquote]

[Prose paragraph: what it does, what problem it solves, how it works at a high level.
2–4 sentences. Mention the core technology and key differentiating architecture.]

## Features

- **[Feature name]** — [fragment description]
- **[Feature name]** — [fragment description]
- **[Feature name]** — [fragment description]

## Architecture

```
[mermaid or ASCII diagram in a code block]
```

## Installation

```
# [Method / OS]
pip install -e .

# With optional dependency
pip install -e ".[extra]"

# Requirements note
```

## Quick Start

### [Platform 1] ([backend name])

```
# 1. [Step with comment]
[command]

# 2. [Step with comment]
[command]
```

### [Platform 2] ([backend name])

```
[platform-specific commands]
```

### [Optional: MCP / API mode]

```
[server start + example curl]
```

## [Command Reference or Broker Commands]

| Command | Description |
|---|---|
| `[cmd]` | [what it does] |

## [Profiles / Modes / Providers]

| Name | [Column] | Description |
|---|---|---|
| `[name]` | [value] | [Em-dash description] |

## [Core Concept Section — e.g., Human Intervention]

[1–2 sentence explanation of the concept]

```
[state diagram or flow in code block]
```

**Workflow:**

1. [Step]
2. [Step]
3. [Step]

## [API Reference — if tool exposes HTTP/RPC interface]

[Request format code block]

### [Tool/Method name]

[One-line description]

| Parameter | Type | Default | Required | Description |
|---|---|---|---|---|
| `param` | type | default | Yes/No | description |

**Returns:** `{ "field", "field" }`

```
[example curl]
```

## CLI Reference

```
usage: [command] [options] {subcommands}
```

| Subcommand | Description | Key Arguments |
|---|---|---|
| `[cmd]` | [what] | `--flag value` |

## Testing

```
# Install dev dependencies
[install command]

# Run tests
[test command]

# Additional test modes
[command]    # description
```

## 🤖 AI-Assisted Development

[boilerplate with model table]

## License

[MIT License](link)
```

---

## Key style notes for cli-tool

- **No banner image required** — CLI tools are code-first; banner is optional. If the project has visual branding, include it; if not, skip it.
- **No ALL CAPS H1, no emoji H2** — clean markdown headers only, no emoji.
- **Blockquote tagline** — always use `>` blockquote for the one-liner, not bold.
- **Prose intro paragraph** — 2–4 sentences of flowing prose before jumping into features. The only template type that uses prose instead of a table for the opening.
- **Platform-split Quick Start** — always split by OS/backend if the tool supports multiple. Use `### Linux / macOS` and `### Windows` headers.
- **Mermaid or ASCII diagrams** — Architecture section expects a diagram in a code block. Mermaid preferred if supported; ASCII fallback.
- **API reference tables** — if the tool has an HTTP/RPC interface, document every endpoint with the full parameter table and example curl.
- **State diagrams for workflows** — Human intervention, approval flows, state machines: always use a diagram (mermaid stateDiagram-v2 or ASCII state diagram).
- **AI-Assisted section** — table format with Model | Role columns. List specific roles like "Primary architect and implementation".
- **繁體中文 link** — at top, as standalone linked line (no nav row needed for simpler docs).
