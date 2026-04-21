# UniText — Vision

> Statut : `Template Base`
> Principe : s’appuyer sur des contrats logiques, pas sur un système d’exploitation, une arborescence ou un mode de déploiement unique.

## 1. Ce qu’est UniText

`UniText` est un shared resource hub text-native, registry-first et AI-first. Il permet à plusieurs systèmes AI CLI / agents de partager la même définition de ressources et le même modèle d’adoption à travers un contrat purement textuel.

Il contient deux couches :

1. `Registry`
   - définit les shared resources, l’identité canonique et le contrat minimal
2. `Adapter / Operations Control Plane`
   - relie le contenu du registry aux différents CLI et gère `install`, `sync`, `adopt`, `repair`

## 2. Le problème résolu

`UniText` résout la fragmentation habituelle du partage de ressources entre outils :

- les skills sont dispersés à plusieurs endroits
- les définitions MCP existent dans différents formats de configuration
- les instructions d’agent ne peuvent pas être partagées facilement
- les conventions de workflow se perdent d’un outil à l’autre
- il manque une interface textuelle commune, lisible par les IA et compatible avec le versionnage

## 3. Positionnement architectural

Position officielle :

**Registry-first, adapter-enabled, operations-governed**

Principes clés :

- sans registry, il n’existe ni source commune ni sémantique commune
- sans adapter, le registry ne peut pas être livré aux différents CLI
- l’IA est un consommateur et un collaborateur important, mais pas le seul mécanisme d’intégration fiable

## 4. Types de ressources

Types partagés par défaut :

- `skills`
- `mcp`
- `agents`
- `workflow`

`operations state` ne fait pas partie des shared resource types et doit vivre séparément dans `/operations`.

## 5. Discovery et delivery

`INDEX.md` gère la discovery et répond à :

- quelles ressources existent
- où se trouve l’emplacement logique de chaque ressource
- quels CLI sont pris en charge

`OPERATIONS.md` gère la delivery et répond à :

- comment un CLI obtient une ressource
- quand exécuter `install`, `sync`, `adopt`, `repair`
- comment interpréter le delivery mode

Delivery modes disponibles :

- `pointer`
- `mirror`
- `symlink`
- `native-config`

## 6. Déclencheurs de delivery

La delivery ne peut être déclenchée que par un trigger explicite :

- `bootstrap`
- `sync`
- `adopt`
- `repair`

Toute opération destructive doit respecter :

- d’abord un `dry-run`
- d’abord une sauvegarde
- aucune décision silencieuse sur la source canonique

## 7. Modèle d’adoption

### Adoption souple

- commencer par la découverte
- ne pas forcer immédiatement la migration des ressources existantes

### Adoption formelle

Flux officiel de gouvernance :

1. `SCAN`
2. `REVIEW`
3. `DRY-RUN`
4. `ADOPT`
5. `DELIVER`
6. `VERIFY`

Si deux ressources portent le même nom mais un contenu différent, le flux doit s’arrêter en `REVIEW / DRY-RUN`.

## 8. Ensemble documentaire

Documents centraux :

- `VISION.md`
- `INDEX.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`

## 9. Stratégie de chemins

Le document principal utilise des logical canonical paths, par exemple :

- `/registry/skills`
- `/registry/mcp`
- `/registry/agents`
- `/registry/workflow`
- `/operations`

Les chemins absolus et les paramètres spécifiques à une plateforme n’appartiennent qu’au deployment mapping, pas au contrat de vision.

## 10. Principes de conception

- `Registry first`
- `Discovery before automation`
- `Explicit triggers`
- `Minimum viable metadata`
- `Canonical source of truth`
- `CLI-specific delivery`
- `Platform-agnostic contract`
- `Safe mutation`

## 11. Positionnement en une phrase

> UniText est un shared resource hub text-native, registry-first et AI-first, qui permet à plusieurs AI CLI de découvrir, adopter et partager en sécurité les mêmes canonical resources grâce à un adapter clair et à un operations control plane.
