# Template: Local Utility / Windows Launcher / Installer Script

Reference project: `nano-otter-runtime`
Characteristics: PowerShell/Bash scripts, Windows-first, local tool, no npm/pip publish, research/exploration project

---

## Section order

```
[Banner image]

# [Project Name — Title Case]

> **[繁體中文版](README.zh-TW.md)**

[One sentence: what it does and its primary value.]

## Background

[2–4 sentences of factual context explaining WHY this tool exists.
What triggered the need? What did the author discover? What gap does it fill?
This section should read like a technical brief, not marketing copy.]

> [Optional: blockquote for a key finding or data point]

## Screenshots

[![alt](path)](path) 
[![alt](path)](path)

[Short label]  |  [Short label]

## Features

- [Specific, concrete feature — not vague]
- [Specific feature]
- [Specific feature]

## Quick Start

1. Run `[main script]` from the project root.
2. [Second step — numbered, concrete]
3. [Third step with URL or output example]
4. [Fourth step if needed]

## [Core Concept / Main System — e.g., "NANO Exchange Layer"]

[1–2 sentence description of the key architectural concept]

- `[component]`: [what it does — em-dash style]
- `[component]`: [what it does]
- `[component]`: [what it does]

## [Secondary Concept / Scenario — e.g., "Multi-Party Scenario"]

[Brief description]

Built-in [entities/modes/profiles]:

```
[list or code block showing the built-in configurations]
```

Run method:

1. [Step]
2. [Step]
3. [Step]

## [Data / Model / Config Files — if applicable]

> ⚠️ **[Important warning about sensitive files / exclusions]**

[Explanation of where files live and what to include/exclude]

```
[directory structure or path]
```

### [Sub-section: Locating / Importing]

```
[shell command]
```

### [Sub-section: Required Files]

[Table or list of required files with paths]

### [Sub-section: Safety Check]

```
[verification commands]
```

## [Runtime Modes or Operation States]

| Mode | Description |
|---|---|
| `[Mode name]` | [Em-dash description] |

[Troubleshooting tip if a mode is commonly stuck]

## Key Files

| File | Description |
|---|---|
| `[filename]` | [what it does] |
| `[filename]` | [what it does] |

## Manual Commands

```
[explicit commands for users who prefer manual operation]
```

## 🤖 AI-Assisted Development

[boilerplate with model table]

### Human Oversight

- [Specific oversight action taken]
- [Specific verification step]
- [Policy on what was manually reviewed]
- [Git / data safety note]

> ⚠️ **Disclaimer:** [standard text]

## License

[MIT License](link)
```

---

## Key style notes for utility-installer

- **Banner image is standard** — these projects often have a custom banner or diagram; include it.
- **Title case H1** — not ALL CAPS. These are technical tools, not consumer products.
- **繁體中文 as standalone bolded link** — `> **[繁體中文版](README.zh-TW.md)**` directly after H1, as a blockquote.
- **Background section is unique to this type** — required. It establishes credibility and explains the discovery or security context behind the tool.
- **Screenshots with side-by-side caption** — use the pattern: `Left: [label]  |  Right: [label]` as plain text after the images.
- **Quick Start uses numbered steps** — not code blocks for the steps themselves; the steps are prose with inline `code` references.
- **Key Files table** — two-column file manifest is required; these projects have non-obvious file structures.
- **AI-Assisted includes Human Oversight subsection** — bullet points listing specific review actions taken. More detailed than other project types.
- **No navigation anchor row** — these are shorter docs; navigation links are unnecessary.
- **No Architecture diagram** — complexity is presented through file tables and step lists, not diagrams.
- **Warning blockquotes for data safety** — any section dealing with sensitive files (model weights, credentials, local data) gets a `> ⚠️` warning.
