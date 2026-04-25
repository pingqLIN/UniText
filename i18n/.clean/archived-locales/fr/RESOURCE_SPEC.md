# UniText — Spécification des ressources

> Statut : `Template Base`
> Périmètre : contrat logique pour les shared resources, sans dépendre d’un système d’exploitation, d’une arborescence ou d’un format de stockage unique.

Cette spec part du principe que toutes les métadonnées essentielles peuvent être transportées de manière stable en texte brut, afin que les humains et les IA puissent les lire, les comparer et les versionner facilement.

## 1. Scope

Cette spec s’applique à :

- `skills`
- `mcp`
- `agents`
- `workflow`

Elle ne s’applique pas à :

- les operations state artifacts
- les mappages de chemins spécifiques à une plateforme
- les détails d’exécution internes d’un adapter

## 2. Règles d’identité

L’identité principale d’une shared resource est composée de :

- `type`
- `id`

`id` doit :

- utiliser des lettres minuscules, des chiffres et `-`
- ne contenir aucun espace
- ne contenir aucun séparateur spécifique à un système d’exploitation

## 3. Canonical Location

`canonical_location` doit être un logical canonical path, pas un chemin absolu propre à une machine.

Exemples :

- `/registry/skills/example-skill`
- `/registry/mcp/example-mcp`
- `/registry/agents/example-agent`

## 4. Niveaux de métadonnées

### Obligatoires

- `id`
- `type`
- `canonical_location`
- `status`

### Recommandés

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

### Optionnels

- `owner`
- `provenance`
- `notes`
- `last_verified`

## 5. Cycle de vie

Statuts autorisés pour `status` :

- `draft`
- `active`
- `deprecated`
- `archived`

## 6. Valeurs par défaut

- si `source_of_truth` est absent, il est considéré comme égal à `canonical_location`
- si `supported_clis` est absent, il est considéré comme `undocumented`
- si `delivery_guidance` est absent, il est déduit à partir des documents d’adapter / operations

## 7. Delivery Guidance

`delivery_guidance` est une indication pour la discovery, pas un delivery mode figé.

Il peut préciser :

- quel type d’adapter consulter
- s’il existe des différences entre plateformes
- s’il faut lire `OPERATIONS.md`

Il ne doit pas figer :

- des chemins absolus de plateforme
- un delivery mode permanent et immuable

## 8. Règles de conflit

Si un même couple `(type, id)` correspond à plusieurs ressources candidates dont le contenu diffère :

- ne pas écraser automatiquement
- ne pas supposer silencieusement la source canonique
- s’arrêter en `REVIEW / DRY-RUN`

Résultats possibles :

- choisir explicitement la source canonique
- renommer avec un autre `id`
- marquer comme `deprecated` ou `archived`
- conserver temporairement l’état `draft`

## 9. Exemple

```yaml
id: example-skill
type: skills
canonical_location: /registry/skills/example-skill
status: draft
source_of_truth: /registry/skills/example-skill/SKILL.md
supported_clis: undocumented
delivery_guidance: Use the skills adapter; resolved mode depends on CLI capabilities and local environment.
```

