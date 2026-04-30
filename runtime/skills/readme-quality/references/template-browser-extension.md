---
runtime_projection: true
source_of_truth: registry/skills/readme-quality/references/template-browser-extension.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/readme-quality/references/template-browser-extension.md`
> Source of truth: `registry/skills/readme-quality/references/template-browser-extension.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Template: Browser Extension

Reference project: `Falcon-Player-Enhance`
Characteristics: manifest.json, MV3, Chrome extension, rich feature set, dashboard UI

---

## Section order

```
[Banner image]

[badges: manifest version · version number · license · platform]

**Bold tagline — one sentence describing the core function.**

[Quick Start](#anchor) · [Features](#anchor) · [Screenshots](#anchor) · [Shortcuts](#anchor) · [Architecture](#anchor) · [Development](#anchor) · [繁體中文](README.zh-TW.md)

---

## Overview

**[Project Name]** is a [platform] extension purpose-built for **[core function]**.
[One sentence on what problem it solves and how it relates to similar tools.]

| Capability | Description |
|---|---|
| 🛡️ **[Feature]** | [Em-dash description of what it does] |
| 🚫 **[Feature]** | [Em-dash description] |
| 🎬 **[Feature]** | [Em-dash description] |
| ⌨️ **[Feature]** | [Em-dash description] |

> 💡 **Recommended:** [Companion tool suggestion if applicable.]

---

## 🚀 Quick Start

### Installation

```
1. [Step]
2. [Step]
3. [Step]
4. [Step]
```

### [Optional: Provider / API Setup]

| Provider | Type | Setup |
|---|---|---|
| **[Name]** | [Type] | [How] |

See [INSTALL.md](INSTALL.md) for detailed setup.

---

## ✨ Features

### [Feature Group with emoji]

| Layer/Feature | [Column] | Description |
|---|---|---|
| **[Sub-feature]** | [value] | [Em-dash description] |

### [Feature Group with emoji]

| Feature | Description |
|---|---|
| **[Sub-feature]** | [Em-dash description] |

---

## 📸 Screenshots

### [UI Name]

[![alt](path)](path)

*Caption — what's shown*

[![alt](path)](path)

*Caption — what's shown*

> 📖 For a complete visual guide, see **[FEATURE_GUIDE.zh-TW.md](docs/FEATURE_GUIDE.zh-TW.md)**.

---

## ⌨️ Keyboard Shortcuts

When [condition], these shortcuts are automatically activated:

### [Group]

| Key | Action |
|---|---|
| `Key` | [Description] |

---

## 🏗 Architecture

```
[directory tree — code block]
```

### Module Overview

| Module | World | Role |
|---|---|---|
| `file.js` | [world] | [Em-dash description] |

### Message Flow

```
[ASCII flow diagram]
```

---

## 🧪 Development

### Test Commands

```
npm run test:[name]    # description
```

### Tech Stack

- **Platform:** [name]
- **APIs:** [list]
- **Languages:** [list]
- **[Other]:** [list]

---

## 📄 Documentation

| Document | Description |
|---|---|
| [link] | [description] |

---

## 🤝 Contributing

Contributions are welcome! Please open an Issue first to discuss proposed changes.

---

## 🤖 AI-Assisted Development

[boilerplate]

---

## 📜 License

[MIT License](LICENSE)
```

---

## Key style notes for browser-extension

- **Emoji H2 headers are mandatory** — every major section gets a leading emoji.
- **No ALL CAPS H1** — title case only for extensions.
- **Blockquote companion tool tip** — if the extension complements another tool, always include a `> 💡 **Recommended:**` tip in the Overview section.
- **Overview table always has 4 columns minimum** — emoji + bold feature name + description.
- **Screenshots section** — must include at least the main UI and the dashboard. Use `*italic caption*` beneath each image.
- **Directory tree in code block** — `🏗 Architecture` always includes the actual file tree with inline comments.
- **Module + Message Flow** — two subsections under Architecture are expected.
- **Documentation table** — list all companion `.md` files, especially zh-TW guides.
- **AI-Assisted section** — include both models used and their specific roles (e.g., "architecture review, UI redesign, documentation").
