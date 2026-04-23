[English](../../DOCUMENT_PLACEMENT_POLICY.md) | [繁體中文](../zh-TW/DOCUMENT_PLACEMENT_POLICY.md) | [简体中文](../zh-CN/DOCUMENT_PLACEMENT_POLICY.md) | [日本語](../ja/DOCUMENT_PLACEMENT_POLICY.md) | [Deutsch](../de/DOCUMENT_PLACEMENT_POLICY.md) | [Français](DOCUMENT_PLACEMENT_POLICY.md) | [Español](../es/DOCUMENT_PLACEMENT_POLICY.md) | [한국어](../ko/DOCUMENT_PLACEMENT_POLICY.md) | [Italiano](../it/DOCUMENT_PLACEMENT_POLICY.md)

# UniText — Politique de placement des documents

> Statut : Active Baseline
> Usage : définit dans quelle couche placer les documents de gouvernance, de référence, d'authoring et d'operations afin d'éviter de mélanger shared content et live workspace content.

## 1. Purpose

UniText est en même temps :

- un authoring workspace
- une shared registry baseline
- une source d'export template / rebuild

Si l'on classe les documents uniquement par sujet, il devient facile de les placer dans la mauvaise couche.

Cette règle répond à :

- quels types de documents doivent aller dans `registry/`
- quels types de documents doivent aller dans `local/`
- quels types de documents doivent aller dans `ops/`
- quels documents peuvent être tracked
- quels documents doivent rester uniquement dans l'espace local authoring ignoré

## 2. Core Rule

Pour décider de l'emplacement d'un document, il faut regarder d'abord la nature du contenu, pas le domaine du sujet.

- si le document décrit une shared canonical truth, il va dans la shared layer
- s'il décrit l'état actuel d'un seul authoring workspace, il va dans la local layer
- s'il décrit un historique d'opérations, un résultat d'export, une audit evidence ou un generated state, il va dans la operations layer

Le fait qu’un document ait été rédigé dans une « fenêtre de travail » donnée ou sur une machine d’authoring donnée n’est pas le critère principal.

- Le fait d’être rédigé dans le UniText authoring workspace ne signifie pas automatiquement `local/docs/authoring/`
- Le fait d’être tracked ne signifie pas non plus automatiquement « publiable » ou « poussable »
- Demandez d’abord à qui sert le document et quelle couche de vérité il décrit, puis décidez de son emplacement

## 3. Placement Matrix

| Content type | Canonical location | Tracked | Share-safe | Notes |
|---|---|---|---|---|
| principes d'architecture, règles de gouvernance, specs template-safe | root docs ou `registry/` | Yes | Yes | doivent éviter les live workspace values |
| shared sanitized reference | `registry/.../references/` | Yes | Yes | la structure peut être décrite, mais les valeurs doivent être redacted ou remplacées par des placeholders |
| shared workflow / runbook / template | `registry/workflow/` | Yes | Yes | ne doit pas être lié à une seule machine auteur |
| machine-local path map / wiring notes | `local/docs/` | Case-by-case | Usually no | location / state autorisés, pas de plaintext secret |
| live workspace baseline | `local/docs/*_WORKSPACE_BASELINE.md` | No | No | doit être ignoré |
| live operational checklist | `local/docs/*_LIVE.md` | No | No | doit être ignoré |
| authoring plans / drafts / review notes | `local/docs/authoring/` | No | No | doit être ignoré |
| generated audit trail / export output / drift report | `ops/` | No | No | relève du state, pas d'une canonical source |

## 4. Naming Rules

Si un sujet a besoin d'une version shared et d'une version live, utiliser par défaut un nommage par paire :

- shared sanitized doc
  - `registry/.../references/<topic>.md`
- live workspace doc
  - `local/docs/<TOPIC>_WORKSPACE_BASELINE.md`
  - ou `local/docs/<TOPIC>_LIVE.md`

## 5. Pair Rule

Quand shared sanitized doc et live workspace doc coexistent, il faut respecter :

1. la version shared ne garde que la structure template-safe et des redacted placeholders
2. la version live reste uniquement dans `local/docs/` ou `local/docs/authoring/`
3. la version shared doit indiquer l'emplacement de la version live
4. la version live doit aussi pointer vers la shared sanitized reference correspondante

## 6. Publishing Rule

Ces affirmations ne doivent pas être confondues :

- template export passes
- rebuild export passes
- branch is publish-safe

Le fait qu'un export template / rebuild soit propre signifie seulement que l'artefact exporté a une frontière plus propre. Cela ne veut pas dire que tout le tracked content du repo d'authoring est sûr à pousser.

## 7. Quick Decisions

Si tu hésites sur l'emplacement d'un document, pose d'abord ces trois questions :

1. ce document décrit-il à quoi ressemble actuellement un authoring workspace unique ?
   - oui : privilégier `local/docs/`
2. ce document est-il un résultat d'opération, un artefact d'audit, un paquet exporté ou un drift report ?
   - oui : privilégier `ops/`
3. ce document doit-il pouvoir être référencé de manière sûre par template / rebuild / shared registry ?
   - oui : privilégier les root docs, `registry/` ou la shared workflow layer

## 8. Decision Ladder

Si vous avez besoin d’une décision plus stable, suivez cet ordre :

1. S’agit-il d’un generated state, d’une audit evidence, d’un drift report ou d’un export output ?
   - oui : va dans `ops/`
2. Décrit-il un authoring workspace unique, une machine unique ou le live wiring actuel ?
   - oui : va dans `local/docs/`
3. S’il décrit un workspace unique, est-ce un draft, une review note ou un authoring workboard ?
   - oui : va dans `local/docs/authoring/`
4. Est-ce une canonical truth destinée à être réutilisée par de futurs shared readers, et doit-elle être template-safe ?
   - oui : va dans la tracked shared layer
5. Si cela relève de la tracked shared layer, à quel type ressemble-t-il le plus ?
   - repo-wide policy / spec : va dans les root docs
   - sanitized reference : va dans `registry/.../references/`
   - shared workflow / runbook : va dans `registry/workflow/`
6. Si une version shared et une version live doivent coexister
   - créez un sanitized/live pair ; ne mélangez pas les deux frontières dans un seul fichier

Si vous hésitez encore, utilisez :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\get-document-placement-recommendation.ps1 -Topic "cloudflare workflow" -CanonicalSharedTruth -SharedForm registry-reference
```

## 9. Common Misplacements

- placer une live Cloudflare baseline dans `registry/.../references/`
- placer un strategy / review plan à la racine
- traiter un export output ou une audit evidence comme une canonical reference
- écrire des machine-specific paths directement dans les shared governance docs

## 10. Review Gate

Avant d'ajouter un document de governance / reference, il faut au minimum vérifier :

- qu'il décrit une shared truth et non un live workspace state
- qu'un push resterait conforme à `NO_PUBLISH_POLICY.md` et aux attentes template-safe
- qu'il ne faut pas plutôt un couple sanitized/live au lieu d'un seul fichier qui mélange les deux

## 11. Related Docs

- `README.md`
- `INDEX.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `NO_PUBLISH_POLICY.md`
