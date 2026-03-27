[English](../../README.md) | [繁體中文](../zh-TW/README.md) | [简体中文](../zh-CN/README.md) | [日本語](../ja/README.md) | [Deutsch](README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [한국어](../ko/README.md) | [Italiano](../it/README.md)

# UniText

> **Ein text-natives, registry-first Shared-Resource-Hub für mehrere AI CLIs.**
>
> Reiner Text als gemeinsame Schnittstelle, damit Claude Code, Codex, Gemini CLI und andere Tools dieselben Ressourcendefinitionen nutzen können.

## 2026-03-27 Synchronisierungshinweis

Für den aktuellen Baseline-Stand dieser Übersetzung sind vor allem diese Punkte maßgeblich:

- die Support-Labels heißen jetzt `verified` / `partial` / `target`
- `Copilot CLI` ist derzeit `target` / `adapter pending`
- die Material-Sets werden als `authoring review shortlist`, `public release subset` und `local-only validation materials` unterschieden

Falls diese Übersetzung vom englischen Hauptdokument abweicht, gilt das [English README](../../README.md) als authoritative version.

---

## Warum es das gibt

Wenn du mehr als ein AI-CLI-Tool verwendest, verteilen sich deine Ressourcen schnell:

- dieselbe Skill dreimal definiert, jeweils in leicht unterschiedlichem Zustand
- MCP-Server-Konfigurationen in Formaten, die andere Tools nicht lesen können
- Agent-Anweisungen, die nur eine CLI kennt
- keine verlässliche Aussage darüber, welche Kopie die kanonische ist

UniText löst das mit einem gemeinsamen Registry und einer gesteuerten Delivery-Schicht. **Eine Definition. Jedes Tool.**

---

## Wie es funktioniert

```text
UniText/
├── registry/          ← kanonische Definitionen (was existiert)
│   ├── skills/        ← gemeinsame Skill-Definitionen
│   ├── mcp/           ← MCP-Server-Definitionen
│   ├── agents/        ← Agent-Anweisungen & Personas
│   └── workflow/      ← Runbooks, Pläne, Konventionen
│
├── local/             ← Deployment-Overlay (wie es hier verdrahtet ist)
│   ├── docs/          ← Pfadkarten, Deployment-Notizen
│   └── scripts/       ← Sync-Skripte für diesen Rechner
│
└── ops/               ← Operations-Status (keine geteilten Ressourcen)
    └── history/       ← zeitgestützter Audit-Trail
```

Die `registry/`-Schicht ist plattformunabhängig - sie verwendet logische kanonische Pfade (`/registry/skills`, `/registry/mcp`) statt betriebssystem-spezifischer absoluter Pfade. Die `local/`-Schicht löst diese auf deinen tatsächlichen Rechner auf.

---

## Architektur

**Registry-first, adapter-enabled, operations-governed.**

| Layer | Rolle |
|-------|------|
| **Registry** | Definiert, welche Shared Resources existieren und welche kanonische Identität sie haben |
| **Adapter** | Liefert Registry-Inhalte an jede CLI aus (Mirror, Symlink, Native Config, Pointer) |
| **Operations** | Steuert, wann und wie Mutationen stattfinden - mit Backup, Dry-Run und Audit-Trail |

### Ressourcentypen

| Typ | Logische Wurzel | Was hier hineinkommt |
|------|----------------|----------------------|
| `skills` | `/registry/skills` | geteilte Skill-Definitionen für AI Agents |
| `mcp` | `/registry/mcp` | MCP-Server-Definitionen, CLI-übergreifend |
| `agents` | `/registry/agents` | Agent-Anweisungen, Personas, System-Prompts |
| `workflow` | `/registry/workflow` | Runbooks, Planvorlagen, Konventionen |

### Delivery-Modi

Jede Ressource kann je nach CLI-Fähigkeit unterschiedlich ausgeliefert werden:

- `pointer` - nur Discovery, keine Inhaltskopie
- `mirror` - lokale Kopie via robocopy/rsync
- `symlink` - fester Pfadlink auf die kanonische Quelle
- `native-config` - Registrierung im nativen Konfigurationsformat der CLI

---

## Erste Schritte

### 1. Dieses Repository forked oder klonen

```bash
git clone https://github.com/your-username/UniText.git
cd UniText
```

### 2. Erste Ressource hinzufügen

Lege einen Skill unter `registry/skills/` an:

```text
registry/skills/my-skill/
└── SKILL.md
```

Minimales `SKILL.md`:

```yaml
---
name: my-skill
description: Was dieser Skill in einem Satz macht
---

## Usage

Anweisungen für den AI-Agenten...
```

### 3. Im Katalog registrieren

Füge einen Eintrag in `INDEX.md` hinzu:

| Feld | Wert |
|-------|------|
| `id` | `my-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/my-skill` |
| `status` | `active` |
| `supported_clis` | `claude, codex, gemini` |

### 4. Lokales CLI-Wiring bootstrappen

Bevorzuge den plattformübergreifenden Bootstrap-Pfad:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

`bootstrap.py` richtet die gemeinsamen Skills-Ziele aus, aktualisiert den Codex-`skills_path` und schreibt eine projektlokale `.mcp.json` für das mitgelieferte MCP-Baseline-Modell. `sync-skills.ps1` bleibt als Windows-PowerShell-Referenzimplementierung erhalten.

---

## Unterstützte CLIs

UniText verwendet in diesem Repository drei Support-Labels:

- `verified`
  - für den angegebenen Umfang existiert wiederholbare Repo-Evidenz
- `partial`
  - es gibt Teilvalidierung, aber das Repo behauptet noch keine vollständige End-to-End-Abdeckung
- `target`
  - nur beabsichtigte Support-Oberfläche; in diesem Repo noch nicht verifiziert

| CLI | Support Class | Verification Scope | Hinweise |
|-----|---------------|--------------------|----------|
| **Claude Code** | `verified` | `delivery path verified` | `.claude/settings.json`, die projektlokale `.mcp.json` und der Shared-Skills-Lieferpfad gehören zur gepflegten Baseline; dies wird noch nicht als End-to-End-Task-Verifikation behauptet |
| **Gemini CLI** | `verified` | `delivery path verified` | der Shared-Skills-Lieferpfad gehört zur gepflegten Baseline; End-to-End-Interaktion wird derzeit nicht behauptet |
| **Codex** | `partial` | `bootstrap path defined` | Native-Config-Wiring ist über `bootstrap.py` und `config.toml` implementiert, aber dieses Repo beansprucht noch keine vollständig wiederholbare End-to-End-Bootstrap-Verifikation auf frischen Maschinen |
| **Copilot CLI** | `target` | `adapter pending` | soll die gemeinsame MCP-/Skill-Baseline konsumieren, sobald ein stabiler Repo-Level-Adapterpfad definiert ist |

Siehe [template/examples/local/README.md](../../template/examples/local/README.md) für das Starter-Local-Overlay, einschließlich `template/examples/local/docs/PATH_MAP.template.md`.
Siehe [local/docs/SUPPORT_PROOF_MATRIX.md](../../local/docs/SUPPORT_PROOF_MATRIX.md) für die aktuelle Zuordnung zwischen Support-Claims und Proof-Artefakten.

Wenn du dieses Repository in ein sauberes neues Starter-Projekt umwandeln willst, statt direkt den Authoring-Workspace zu verwenden, folge [REBUILD_AS_NEW_PROJECT.md](../../REBUILD_AS_NEW_PROJECT.md).

### Plattformübergreifende Baseline

Das GitHub-hosted Starter-Template hat eine breitere Zieloberfläche als die aktuell verifizierte Oberfläche.

| Plattform | Support Class | Verification Scope | Hinweise |
|----------|---------------|--------------------|----------|
| `Windows` | `verified` | `authoring + export baseline verified` | aktuelle Skripte, der Review-Export-Flow und der Template-Export-Flow werden auf Windows gepflegt und revalidiert |
| `macOS` | `target` | `template target` | der Python-basierte `bootstrap -> verify`-Pfad ist auf Portabilität ausgelegt, aber dieses Repo behauptet noch keine wiederholte macOS-Evidenz |
| `Linux` | `target` | `template target` | der Python-basierte `bootstrap -> verify`-Pfad ist auf Portabilität ausgelegt, aber dieses Repo behauptet noch keine wiederholte Linux-Evidenz |

Die versionierte `.mcp.json` ist ein relativer Seed für frische Klone. Der unterstützte First-Run-Pfad bleibt:

```bash
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

Keine Plattform in diesem README sollte als `end-to-end verified` gelesen werden, sofern dies nicht ausdrücklich so gesagt wird.

### Aktuelle Material-Sets

UniText unterscheidet derzeit drei Material-Sets:

- `authoring review shortlist`
  - maintainer-orientiertes Working Set zum Review und Vergleich von Candidate Skills
- `public release subset`
  - GitHub-backed, öffentlich redistributable Teilmenge, die in exportierten Review-Packages ausgeliefert werden kann
- `local-only validation materials`
  - maintainer-lokale oder nicht für Release bestimmte Materialien, die in Dry-Run-Validierung genutzt werden können, aber nicht zur öffentlichen Release-Oberfläche gehören

Wenn diese Sets voneinander abweichen, ist das exported package die release truth, nicht der Authoring-Workspace.

---

## Governance-Regeln

UniText setzt eine **No Silent Changes**-Policy durch:

1. **Nur explizite Trigger** - `bootstrap`, `sync`, `adopt`, `repair`
2. **Backup vor jeder Mutation** - jede destruktive Aktion erstellt einen zeitgestempelten Snapshot in `ops/`
3. **Dry-Run vor Delivery** - vor der Ausführung anzeigen, was sich ändern wird
4. **Konflikte stoppen den Flow** - wenn zwei Versionen derselben Ressource abweichen, stoppt das System für menschliche Prüfung
5. **Vollständiger Audit-Trail** - jede Operation wird in `ops/history/` protokolliert

Formaler Adoption-Flow: `SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY`

---

## Dokumentation

| Datei | Zweck |
|------|------|
| [INDEX.md](INDEX.md) | Discovery-Einstiegspunkt - welche Ressourcen es gibt und wo sie liegen |
| [VISION.md](VISION.md) | Architekturprinzipien und Design-Logik |
| [RESOURCE_SPEC.md](RESOURCE_SPEC.md) | Metadatenvertrag für alle Shared Resources |
| [OPERATIONS.md](OPERATIONS.md) | Delivery-Modi, Trigger und Sicherheitsregeln |
| [PROJECT_MODES.md](PROJECT_MODES.md) | Unterscheidung zwischen Authoring-Repo und Projekt-Template |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | Grenzen für Secret-Speicherung, Redaction und Passwort-/API-Key-Handhabung |
| [MILESTONES.md](MILESTONES.md) | Quantifizierte Phasen-Ziele und externe Review-Meilensteine |
| [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) | Kuratierte `8 + 4`-Essential-Skills-Liste für die aktuelle Review-Runde |
| [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) | Reviewer-facing Umfang, Lesereihenfolge und wiederholbarer Package-Export |
| [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md) | Einreichungsnotiz für externe Reviewer |
| [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md) | Kurzfassung des Reviews für schnellen Einstieg |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | Scope, Ausschlüsse und Exportfluss für die Template-Bereinigung |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | Pre-Release-Checkliste für ein Starter Package |
| [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md) | Konzeptnotiz dazu, wie UniText mit skill-0 als Decomposition- und Primitive-Extraction-Projekt zusammenarbeiten kann |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | Lokale Publishing-Grenze für Agents und Mitarbeitende |

Lesereihenfolge: `EXTERNAL_REVIEW_COVER_NOTE.md` → `EXTERNAL_REVIEW_HIGHLIGHTS.md` → `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md` → `MILESTONES.md` → `EXTERNAL_REVIEW_PACKAGE.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `SKILL0_COLLABORATION_VISION.md`

---

## Zwei Nutzungsarten

### Als Starter Template

Forke dieses Repo. Entferne `ops/history/`, `backup/` und lokalrelevante `local/`-Pfade. Fülle `registry/` mit deinen eigenen Skills und MCP-Definitionen. Passe `local/scripts/` an deine Umgebung an.

### Als Referenzimplementierung

Lies die Kerndokumente, um die Architektur zu verstehen. Übernimm die Muster - Registry-Struktur, Ressourcenvertrag, Delivery-Modi, Operations-Audit-Trail - für deine eigene Umgebung.

---

## Design-Prinzipien

- **Registry first** - zuerst definieren, dann liefern
- **Discovery before automation** - erst wissen, was existiert, dann synchronisieren
- **Platform-agnostic contracts** - logische Pfade in den Specs, absolute Pfade nur im lokalen Overlay
- **Minimum viable metadata** - `id`, `type`, `canonical_location`, `status` reichen zum Start
- **Safe mutation** - immer Dry-Run + Backup + expliziter Trigger
- **AI as consumer** - Modelle lesen und nutzen die Registry; sie sind nicht für die Delivery-Garantie verantwortlich

---

## Status

| Komponente | Status |
|-----------|--------|
| Kerndokumentation | Stabil |
| Registry-Struktur | Aktiv - `skills/`, `mcp/`, `workflow/`, `agents/`-Wurzeln vorhanden |
| Skills-Registry | Aktive Baseline - erster kanonischer Block adoptiert, breitere Adoption läuft weiter |
| Agents-Registry | Aktiver Seed - `registry-curator`-Eintrag angelegt |
| MCP-Registry | Aktive Baseline - kanonische Definition plus ausführbarer read-only Server vorhanden |
| Workflow-Registry | Draft-Seed - Workflow-Dokument plus Planvorlage vorhanden |
| Operations-Audit-Trail | Aktiv |
| Sync-, Bootstrap- und Review-Skripte | Aktive Baseline in `local/scripts/` |
| External Review Package | Aktive Baseline - Reviewer-Guide und Export-Skript vorhanden |
| Template Release Cleanup | Release Candidate - Template-Package-Guide, Checkliste, Export- und Verify-Skripte, generic examples und lokales Overlay-Skeleton vorhanden |

---

## Lizenz

MIT

---

*Für Menschen, die mehr als ein AI-Tool nutzen und eine einzige Source of Truth wollen.*

