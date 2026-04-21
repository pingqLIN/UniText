# UniText — Operations

> Statut : `Template Base`
> Rôle : définir les responsabilités de l’adapter / operations control plane, les règles de delivery et les frontières de sécurité.

Toutes les deliverys et mutations doivent s’appuyer sur le contrat texte brut du registry / spec de `UniText` comme source de vérité.

Si une opération implique des mots de passe, clés API, tokens, credentials ou tout autre matériau sensible, appliquez aussi `SECRET_HANDLING_GUIDELINES.md`.

## 1. Scope

Ce fichier couvre :

- les responsabilités de l’adapter
- les delivery modes
- les delivery triggers
- le flux d’adoption
- la dérive / réparation
- le mappage logique vers physique

Ce fichier ne couvre pas :

- le schéma de métadonnées des shared resources
- une implémentation unique propre à une plateforme
- l’historique d’un dépôt d’authoring local

## 2. Delivery Modes

| Mode | Quand l’utiliser |
|---|---|
| `pointer` | pour la discovery ou pour une ressource non enregistrée localement |
| `mirror` | quand le CLI a besoin d’une copie locale, ou si `symlink` est instable |
| `symlink` | quand le CLI a besoin d’un chemin fixe et que l’environnement supporte des liens stables |
| `native-config` | quand le CLI fournit un point d’entrée de configuration officiel pour enregistrer la ressource |

Le `delivery mode` est interprété par l’adapter au moment de l’opération ; ce n’est pas une propriété fixe de la ressource.

## 3. Règles de résolution du delivery

L’adapter doit suivre l’ordre de priorité suivant :

1. si un point d’entrée de configuration officiel existe, privilégier `native-config`
2. si un chemin fixe est nécessaire et que la plateforme supporte les liens stables, utiliser `symlink`
3. si `symlink` n’est pas sûr, utiliser `mirror`
4. si l’objectif principal est la discovery ou l’entrée, utiliser `pointer`

## 4. Delivery Triggers

La delivery ne peut être déclenchée que par un trigger explicite :

- `bootstrap`
- `sync`
- `adopt`
- `repair`

## 5. Règles de sécurité

### Dry-run d’abord

Les opérations suivantes doivent d’abord produire un plan de `dry-run` :

- `adopt`
- `repair`
- tout `sync` qui écraserait un état existant

### Backup avant mutation

Toute opération destructive doit disposer :

- d’un backup ou d’un point de retour équivalent
- d’un journal d’opération traçable
- de conditions d’arrêt en cas d’échec

### Pas de canonisation silencieuse

Si deux ressources portent le même nom mais un contenu différent :

- il faut s’arrêter en revue
- l’opérateur doit décider explicitement de la source canonique

## 6. Flux d’adoption

1. `SCAN`
   - scanner les sources candidates et lister les ressources adoptables ainsi que leur readiness
2. `REVIEW`
   - vérifier la metadata, la qualité du contenu et la légitimité de la source canonique via la checklist de revue
3. `DRY-RUN`
   - prévisualiser les cibles modifiées par l’adoption ou la delivery, et vérifier si un backup est nécessaire
4. `ADOPT`
   - écrire le contenu source dans l’emplacement canonique du registry ; si un écrasement est nécessaire, faire d’abord un backup
5. `DELIVER`
   - faire livrer le contenu du registry vers le CLI cible via l’adapter ; si un état existant est écrasé, conserver un log et un backup
   - si le CLI supporte `native-config`, on peut écrire une config locale machine lors du `bootstrap`, mais la définition canonique reste dans `registry/`
6. `VERIFY`
   - vérifier l’existence des fichiers, la résolution des chemins, le delivery mode et les conditions de chargement du CLI cible

## 6.1 First-Run Baseline

Si l’objectif est de permettre à un nouvel utilisateur de template de réussir une initialisation minimale sur macOS / Linux / Windows, il faut au minimum fournir :

- un `bootstrap` multiplateforme
- un `verify` multiplateforme
- un flux de backup portable pour le dépôt
- une base MCP minimale réellement exécutable

## 7. Operations State

Les éléments suivants appartiennent à l’operations state, pas aux shared resources :

- inventaires
- baselines
- backups
- rapports de dérive
- plans de réparation
- pistes d’audit

Ils doivent vivre sous `/operations` et ne pas être mélangés avec `/registry`.

## 8. Mappage logique vers physique

Les chemins logiques sont un contrat stable ; les chemins physiques sont un mappage spécifique au déploiement.

| Zone logique | Signification | Exemples de mappage physique |
|---|---|---|
| `/registry/skills` | sources canoniques des skills | dossier partagé, sous-dossier du repo, chemin monté |
| `/registry/mcp` | définitions canoniques MCP | dossier de config, racine d’un manifest généré |
| `/registry/agents` | racines canoniques des instructions d’agent | dossier de profils d’agent, bibliothèque de prompts partagée |
| `/registry/workflow` | docs de workflow / runbooks | dossier workflow, docs locaux du projet |
| `/operations` | inventaires, backups, journaux de dérive | dossier ops, store d’état, répertoire d’audit |

