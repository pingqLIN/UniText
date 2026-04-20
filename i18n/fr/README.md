[English](../../README.md) | [繁體中文](../zh-TW/README.md) | [简体中文](../zh-CN/README.md) | [日本語](../ja/README.md) | [Deutsch](../de/README.md) | [Français](README.md) | [Español](../es/README.md) | [한국어](../ko/README.md) | [Italiano](../it/README.md)

# UniText

> **Un shared resource hub text-native et registry-first pour plusieurs AI CLI.**
>
> Une interface textuelle commune pour que Claude Code, Codex, Gemini CLI et d’autres outils partagent la même définition de ressources.

---

## Ce Que Fait Vraiment UniText

UniText n’est pas simplement un dossier rempli de prompts, de skills ou de modèles MCP. C’est une manière gouvernée de conserver une seule canonical definition pour des ressources AI partagées tout en séparant le machine-local wiring, l’activation propre au projet et l’historique opérationnel. L’objectif est d’éviter que chaque CLI ne développe sa propre copie de la même capacité, puis ne dérive progressivement.

C’est pour cela que ce dépôt réunit `registry/`, `local/`, `ops/`, le template export, le rebuild flow, la boundary verification, le bootstrap et les publishability checks dans un même système. UniText cherche réellement à rendre l’outillage AI partagé portable, reviewable et repeatable à travers plusieurs CLI, plusieurs machines et plusieurs étapes du cycle de vie d’un projet.

---

## Pourquoi UniText existe

Si vous utilisez plusieurs outils AI CLI, vos ressources finissent dispersées :

- le même skill défini trois fois, dans trois états légèrement différents
- des configurations de serveur MCP dans des formats qu’aucun autre outil ne peut lire
- des instructions d’agent connues d’un seul CLI
- aucun moyen simple d’identifier la copie canonique

UniText résout ce problème avec un registry partagé unique et une couche de delivery gouvernée. **Une définition. Tous les outils.**

---

## Comment cela fonctionne

```text
UniText/
├── registry/          ← définitions canoniques (ce qui existe)
│   ├── skills/        ← définitions de skills partagées
│   ├── mcp/           ← définitions de serveurs MCP
│   ├── agents/        ← instructions d’agent et personas
│   └── workflow/      ← runbooks, plans, conventions
│
├── local/             ← couche de déploiement locale (comment cela est branché ici)
│   ├── docs/          ← cartes de chemins, notes de déploiement
│   └── scripts/       ← scripts de synchronisation pour cette machine
│
└── ops/               ← état opérationnel (pas des shared resources)
    └── history/       ← journal d’audit horodaté
```

La couche `registry/` est indépendante de la plateforme : elle utilise des logical canonical paths (`/registry/skills`, `/registry/mcp`) plutôt que des chemins absolus spécifiques à un système d’exploitation. La couche `local/` résout ensuite ces chemins vers la machine réelle.

---

## Architecture

**Registry-first, adapter-enabled, operations-governed.**

| Couche | Rôle |
|-------|------|
| **Registry** | Définit quelles shared resources existent et quelle est leur identité canonique |
| **Adapter** | Distribue le contenu du registry à chaque CLI (`mirror`, `symlink`, `native-config`, `pointer`) |
| **Operations** | Gouverne quand et comment les mutations se produisent, avec sauvegarde, `dry-run` et journal d’audit |

### Types de ressources

| Type | Racine logique | Contenu |
|------|---------------|---------|
| `skills` | `/registry/skills` | Définitions de skills partagées par les agents IA |
| `mcp` | `/registry/mcp` | Définitions de serveurs MCP, utilisables entre CLI |
| `agents` | `/registry/agents` | Instructions d’agent, personas, prompts système |
| `workflow` | `/registry/workflow` | Runbooks, modèles de planification, conventions |

### Modes de delivery

Chaque ressource peut être livrée différemment selon les capacités du CLI :

- `pointer` — découverte seulement, sans copie de contenu
- `mirror` — copie locale via `robocopy` / `rsync`
- `symlink` — lien de chemin fixe vers la source canonique
- `native-config` — enregistré dans le format de configuration natif du CLI

---

## Démarrage

### 1. Forkez ou clonez ce dépôt

```bash
git clone https://github.com/your-username/UniText.git
cd UniText
```

### 2. Ajoutez votre première ressource

Créez un skill sous `registry/skills/` :

```text
registry/skills/my-skill/
└── SKILL.md
```

`SKILL.md` minimal :

```yaml
---
name: my-skill
description: What this skill does in one line
---

## Usage

Instructions for the AI agent...
```

### 3. Enregistrez-la dans le catalogue

Ajoutez une entrée dans `INDEX.md` :

| Champ | Valeur |
|-------|--------|
| `id` | `my-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/my-skill` |
| `status` | `active` |
| `supported_clis` | `claude, codex, gemini` |

### 4. Initialisez le câblage local des CLI

Préférez le chemin d’initialisation multiplateforme :

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

`bootstrap.py` aligne les cibles partagées des skills, met à jour `skills_path` pour Codex et écrit un `.mcp.json` local au projet pour la base MCP intégrée. `sync-skills.ps1` reste disponible comme implémentation de référence PowerShell sous Windows.

---

## CLI pris en charge

| CLI | Mode de delivery | Notes |
|-----|------------------|------|
| **Claude Code** | `mirror` / `symlink` | `~/.claude/skills` |
| **Gemini CLI** | `mirror` / `symlink` | `~/.gemini/skills` |
| **Codex** | `native-config` + MCP local au projet | `skills_path` et `[mcp_servers.*]` dans `~/.codex/config.toml` |
| **GitHub CLI** | `native-config` | `config.yml` |

Voir [template/examples/local/docs/PATH_MAP.template.md](template/examples/local/docs/PATH_MAP.template.md) pour la référence complète des chemins par CLI.

---

## Règles de gouvernance

UniText applique une politique de **zéro changement silencieux** :

1. **Déclencheurs explicites uniquement** — `bootstrap`, `sync`, `adopt`, `repair`
2. **Sauvegarde avant toute mutation** — chaque action destructive crée un instantané horodaté dans `ops/`
3. **Dry-run avant delivery** — prévisualisez les changements avant qu’ils n’arrivent
4. **Le conflit stoppe le flux** — si deux versions d’une même ressource diffèrent, l’outil s’arrête pour revue humaine
5. **Piste d’audit complète** — chaque opération est écrite dans `ops/history/`

Flux formel d’adoption : `SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY`

---

## Documentation

| Fichier | Rôle |
|--------|------|
| [INDEX.md](INDEX.md) | Point d’entrée de la découverte — quelles ressources existent et où elles se trouvent |
| [VISION.md](VISION.md) | Principes d’architecture et logique de conception |
| [RESOURCE_SPEC.md](RESOURCE_SPEC.md) | Contrat de métadonnées pour toutes les shared resources |
| [OPERATIONS.md](OPERATIONS.md) | Modes de delivery, déclencheurs et règles de sécurité |
| [PROJECT_MODES.md](PROJECT_MODES.md) | Distinction entre dépôt d’authoring et template de projet |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | Stockage des secrets, masquage et gestion des mots de passe / clés API |
| [MILESTONES.md](MILESTONES.md) | Objectifs de phase quantifiés et jalons de readiness pour la revue externe |
| [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) | Ensemble sélectionné de `8 + 4` skills essentiels pour la vague de revue actuelle |
| [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) | Périmètre, ordre de lecture et flux reproductible d’export du package de revue |
| [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md) | Note de soumission pour les relecteurs externes |
| [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md) | Résumé court de la revue pour une orientation rapide |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | Périmètre de nettoyage du template release, exclusions et flux d’export |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | Checklist de nettoyage avant publication pour un starter package |
| [docs/concepts/SKILL0_COLLABORATION_VISION.md](docs/concepts/SKILL0_COLLABORATION_VISION.md) | Note conceptuelle sur la collaboration entre UniText et skill-0 comme projet de décomposition et d’extraction de primitives |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | Frontière de publication locale d’abord pour les agents et collaborateurs |

Ordre de lecture : `EXTERNAL_REVIEW_COVER_NOTE.md` → `EXTERNAL_REVIEW_HIGHLIGHTS.md` → `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md` → `MILESTONES.md` → `EXTERNAL_REVIEW_PACKAGE.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `docs/concepts/SKILL0_COLLABORATION_VISION.md`

---

## Deux façons de l’utiliser

### Comme starter template

Forkez ce dépôt. Retirez les chemins `ops/history/`, `backup/` et `local/` propres à cette machine. Remplissez `registry/` avec vos propres skills et définitions MCP. Adaptez `local/scripts/` à votre environnement.

### Comme implémentation de référence

Lisez les documents centraux pour comprendre l’architecture. Adaptez les modèles — structure du registry, spécification des ressources, modes de delivery, piste d’audit opérationnelle — à votre propre contexte.

---

## Principes de conception

- **Registry first** — définir avant de livrer
- **Discovery before automation** — savoir ce qui existe avant de le synchroniser
- **Platform-agnostic contracts** — chemins logiques dans les specs, chemins absolus uniquement dans la couche locale
- **Minimum viable metadata** — `id`, `type`, `canonical_location`, `status` suffisent pour démarrer
- **Safe mutation** — `dry-run` + backup + trigger explicite, toujours
- **AI as consumer** — les modèles lisent et exploitent le registry ; ils ne portent pas la garantie de delivery

---

## Statut

| Composant | Statut |
|-----------|--------|
| Documentation centrale | Stable |
| Structure du registry | Active — les racines `skills/`, `mcp/`, `workflow/`, `agents/` sont présentes |
| Registry des skills | Base active — premier lot canonique adopté, adoption plus large encore en cours |
| Registry des agents | Seed active — entrée `registry-curator` créée |
| Registry MCP | Base active — définition canonique plus serveur read-only exécutable présent |
| Registry workflow | Seed de brouillon — document de workflow et modèle de plan présents |
| Piste d’audit des opérations | Active |
| Scripts de sync, bootstrap et revue | Base active dans `local/scripts/` |
| Package de revue externe | Base active — guide pour relecteurs et script d’export présents |
| Nettoyage pour template release | Release candidate — guide du package, checklist, scripts d’export et de vérification, exemples génériques et skeleton local présents |

---

## Licence

MIT

---

*Pour les personnes qui utilisent plusieurs outils IA et veulent une source de vérité unique.*
