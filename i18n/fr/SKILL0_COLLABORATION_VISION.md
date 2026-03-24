# UniText × skill-0 — Vision de collaboration

> Statut : `Concept Draft`
> Objectif : définir la relation entre `UniText` et `skill-0`, les espaces de collaboration, les voies possibles et les mécanismes encore manquants.

## 1. Résumé exécutif

`UniText` et `skill-0` ne sont ni exclusifs ni redondants ; ils peuvent former une relation amont / aval :

- `UniText` gère le **registry / delivery / governance** des shared resources
- `skill-0` absorbe les skills de haut niveau, les découpe et les normalise en un **atomic operation set** plus générique

La meilleure manière de collaborer n’est donc pas de savoir « qui remplace qui », mais plutôt :

**UniText fournit les entrées canoniques et une couche gouvernable, tandis que skill-0 fournit la décomposition / normalisation / recomposition.**

## 2. Chaque projet résout un problème différent

### UniText

`UniText` résout :

- la manière dont une shared resource devient canonique
- la manière de la livrer entre plusieurs AI CLI
- la manière de gérer les changements avec `SCAN -> REVIEW -> DRY-RUN -> ADOPT -> DELIVER -> VERIFY`

Autrement dit :

**problème de distribution / gouvernance**

### skill-0

`skill-0` résout :

- de quels petits blocs opérationnels un skill de haut niveau est réellement composé
- quelles étapes sont réutilisables comme primitives
- quelles descriptions relèvent du wording de surface, et quelles étapes relèvent du cœur opérationnel
- si un skill de haut niveau peut être réassemblé en un ensemble plus petit, plus générique et plus portable

Autrement dit :

**problème d’abstraction / compiler / normalisation**

## 3. Relation entre les deux

Si l’on adopte l’objectif de `skill-0`, le rôle le plus précieux d’`UniText` n’est pas celui d’un simple résultat distribué, mais plutôt :

- une source stable de skills de haut niveau
- un corpus canonique avec identité logique et metadata
- un ensemble de données de skills qu’on peut analyser, comparer et suivre dans le temps

La relation peut donc se résumer ainsi :

| Projet | Rôle principal |
|---|---|
| `UniText` | source of truth canonique pour les shared resources |
| `skill-0` | analyseur / décomposeur / compilateur des skills de haut niveau |

En une phrase :

**UniText conserve les skills, skill-0 les dissèque.**

## 4. Espace de collaboration actuel

Sans modifier le schéma central de `UniText`, les deux projets disposent déjà d’un espace de collaboration :

### 4.1 Utiliser UniText comme corpus d’entrée

`skill-0` peut prendre directement en entrée :

- `registry/skills/*/SKILL.md`
- les metadata de catalogue dans `INDEX.md`
- le contrat d’identité / de canonical location de `RESOURCE_SPEC.md`

L’analyse porte ainsi non pas sur des copies dispersées, mais sur un corpus de skills canoniques plus propre.

### 4.2 Utiliser UniText comme zone de staging gouvernée

Les résultats d’analyse de `skill-0` peuvent d’abord rester hors du registry canonique et être stockés dans :

- `/operations`
- par exemple `ops/analysis/skill-0/`

Avantages :

- on évite de polluer trop tôt le schéma des shared resources
- on peut vérifier si le format d’analyse est stable
- on peut traiter `skill-0` comme un pipeline d’analyse, pas comme une source canonique immédiate

### 4.3 Utiliser le flux de revue d’UniText pour évaluer les sorties dérivées

Quand `skill-0` produit :

- des atom maps
- des ensembles d’étapes normalisées
- des clusters de sous-routines partagées
- des candidats à la recomposition

Ces sorties peuvent d’abord être examinées selon la même logique de revue qu’UniText :

- l’identité est-elle stable ?
- le nommage est-il clair ?
- le mapping avec le skill source est-il traçable ?
- faut-il une décision humaine pour la forme canonique ?

## 5. Modes de collaboration les plus plausibles

### Mode A — skill-0 comme analyseur externe

`skill-0` prend `UniText` comme source de données et produit des rapports d’analyse, sans réécrire le registry.

Usage adapté :

- valider rapidement la méthode de décomposition
- analyser les overlaps entre skills
- repérer les primitives réutilisables

Avantages :

- coût d’intégration minimal
- quasiment aucun changement du schéma de `UniText`

Inconvénients :

- les résultats restent au niveau d’artefacts sidecar
- difficile d’en faire une shared canonical resource

### Mode B — skill-0 comme générateur sidecar

`skill-0` lit `registry/skills` et génère à côté des sidecars lisibles par machine, par exemple :

- `skill.atoms.json`
- `skill.graph.json`
- `skill.coverage.json`

Avantages :

- relation claire entre skill et atomes
- plus facile à outiller qu’un simple rapport texte

Inconvénients :

- la frontière du schéma UniText devient plus délicate
- il faut décider ce qui est canonique et ce qui n’est que généré

### Mode C — les primitives deviennent un type de ressource à part entière

Si la collaboration mûrit, `UniText` peut ajouter une catégorie officielle de ressources, par exemple :

- `/registry/primitives`
- ou `/registry/operations`

Les sorties de `skill-0` ne seraient alors plus de simples artefacts d’analyse ; elles deviendraient des shared resources gérées officiellement par le registry.

Avantages :

- création d’une véritable couche de vocabulaire commun
- possibilité de recomposer plusieurs skills

Inconvénients :

- il faut modifier le modèle de ressources d’UniText
- il faut un nouveau spec de metadata, un flux d’adoption et des règles de vérification

## 6. Ce qui manque aujourd’hui

Les deux projets ne peuvent pas encore s’intégrer profondément de façon naturelle, principalement parce qu’il manque les mécanismes suivants.

### 6.1 Type canonique manquant pour les primitives

`UniText` ne possède pour l’instant que ces types de ressources de premier niveau :

- `skills`
- `mcp`
- `agents`
- `workflow`

Il n’existe pas encore de :

- `primitives`
- `operations`
- `atoms`

Les sorties qui intéressent vraiment `skill-0` n’ont donc pas encore de couche d’accueil de premier niveau dans `UniText`.

### 6.2 Spec de metadata manquante pour les unités atomiques

`RESOURCE_SPEC.md` convient bien aux shared resources de haut niveau, mais il ne définit pas encore :

- l’atom id
- la signature d’opération
- les préconditions / postconditions
- les règles de composition
- la provenance vers le skill source

### 6.3 Flux d’adoption manquant pour les artefacts dérivés

`UniText` possède déjà un flux d’adoption pour les skills, mais pas encore un flux dédié pour traiter :

- un même skill décomposé en plusieurs ensembles d’atomes
- plusieurs skills mappés sur des primitives proches mais non identiques
- la question de savoir si un atome est suffisamment stable pour devenir canonique

### 6.4 Modèle de vérification manquant

Pour que les sorties de `skill-0` entrent dans une collaboration plus formelle, il faut au minimum pouvoir répondre à :

- la décomposition est-elle stable ?
- la recomposition round-trip est-elle possible ?
- y a-t-il vraiment un gain de réutilisation entre skills ?
- ou s’agit-il simplement d’un renommage de descriptions déjà existantes ?

### 6.5 Frontière manquante entre analyse et canon

Il manque encore une règle claire pour distinguer :

- ce qui, dans `skill-0`, n’est qu’analyse
- ce qui peut déjà être considéré comme shared resource canonique

Quand cette frontière n’est pas claire, l’option la plus sûre reste de stocker les résultats dans `ops/analysis/skill-0/`.

## 7. Direction de court terme recommandée

La voie la plus raisonnable à court terme n’est pas de modifier immédiatement le schéma central de `UniText`, mais d’adopter une progression :

**Mode A -> Mode B**

### Phase A — Analyse uniquement

Commencer par :

- utiliser `registry/skills/*/SKILL.md` comme entrée
- produire des rapports de décomposition
- les stocker dans `ops/analysis/skill-0/`

L’objectif n’est pas encore de canoniser, mais de vérifier :

- si l’extraction d’atomes est stable
- si les overlaps entre skills sont bien observables
- quelles primitives méritent d’être conservées

### Phase B — Sidecars stables

Une fois le format stabilisé, introduire :

- des schemas de sidecar
- des règles de nommage
- le lien vers le skill source
- une vérification de base

À ce stade, il n’est toujours pas nécessaire d’ajouter un nouveau type de ressource, mais on peut déjà établir :

- `skill -> atoms`
- `atom -> source skills`

### Phase C — Primitives de premier niveau

Si l’analyse prouve sa valeur, il sera alors pertinent de discuter de l’ajout dans `UniText` de l’une des options suivantes :

- `/registry/primitives`
- `/registry/operations`

Ce n’est qu’à ce moment-là qu’il faudra modifier formellement :

- `VISION.md`
- `RESOURCE_SPEC.md`
- `INDEX.md`
- `OPERATIONS.md`

## 8. Premiers livrables concrets

Si l’on veut que les deux projets commencent à collaborer, la première vague ne doit pas viser une refonte lourde, mais ces quatre éléments :

1. définir un draft de schema de sortie pour `skill-0`
2. prendre 1 à 2 skills du `Core 8` d’UniText comme exemples de décomposition
3. déposer les résultats dans `ops/analysis/skill-0/`
4. comparer :
   - les atomes partagés entre plusieurs skills
   - l’écart entre la description textuelle du skill et la couche atomique
   - la possibilité de recomposer un workflow minimal exploitable

## 9. Lecture stratégique

Si la collaboration réussit, la répartition à long terme sera claire :

- `UniText` devient le hub canonique des shared AI resources
- `skill-0` devient le moteur de normalisation et d’extraction de primitives

Vu en couches système :

| Couche | Projet |
|---|---|
| Gouvernance canonique des ressources | `UniText` |
| Décomposition / normalisation des skills | `skill-0` |
| Future couche de vocabulaire de primitives | Résultat partagé `UniText × skill-0` |

## 10. Position finale

La conclusion la plus précise aujourd’hui est :

**`UniText` et `skill-0` sont fortement liés, mais ils ne font pas double emploi.**

L’un est orienté gouvernance et distribution ; l’autre est orienté décomposition et abstraction.

Par conséquent, la collaboration la plus raisonnable à court terme n’est pas de forcer `skill-0` dans les quatre types de ressources déjà présents dans `UniText`, mais plutôt :

**laisser `skill-0` prendre `UniText` comme corpus d’entrée canonique et stocker d’abord ses résultats dans `ops/analysis/skill-0/`.**

Une fois le format de sortie, la valeur et la méthode de vérification stabilisés, on pourra décider si la couche primitive / operation doit être élevée au rang de nouveau type de ressource canonique.

