# UniText — Note de couverture de la revue externe

> Date : 2026-03-24  
> Positionnement de version : `External Review Submission Draft`

## 1. Objectif de cette soumission

Le but de cette soumission n’est pas de demander aux relecteurs d’évaluer un produit finalisé, mais de vérifier :

- si l’architecture à trois couches `Registry + Adapter + Operations` est cohérente
- si la séparation entre `skills / mcp / agents / workflow` est claire
- si le flux de gouvernance `SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY` est exécutable
- si le groupe de skills sélectionné `8 + 4` représente suffisamment la première baseline canonique d’UniText

## 2. Position actuelle du projet

`UniText` est actuellement positionné comme :

**external-review-ready baseline**

et non comme :

**template release ready**

Autrement dit, le projet dispose déjà :

- de documents centraux prêts pour la revue
- d’une structure de registry canonique vérifiable
- de scripts d’operations minimaux mais exécutables
- d’un groupe sélectionné et de seed resources

Mais il n’a pas encore finalisé :

- la productisation finale du template export
- le nettoyage complet des artefacts local-only
- une validation plus large en multi-CLI et une stratégie de backup distante

## 3. Ordre de lecture recommandé

1. `README.md`
2. `INDEX.md`
3. `VISION.md`
4. `RESOURCE_SPEC.md`
5. `OPERATIONS.md`
6. `MILESTONES.md`
7. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
8. `PROJECT_STATUS_REPORT_2026-03-23.md`

## 4. Focales de revue recommandées

- l’architecture est-elle surconçue, ou garde-t-elle assez de flexibilité ?
- la frontière entre canonical et local overlay est-elle claire ?
- la sélection de la shortlist est-elle pertinente ?
- la profondeur actuelle de `agents / mcp / workflow` suffit-elle à soutenir la prochaine phase ?
- les scripts de gouvernance existants suffisent-ils à constituer une baseline crédible ?
- le nouveau bootstrap cross-platform et la base MCP soutiennent-ils assez bien un premier utilisateur non auteur ?

## 5. Clarification supplémentaire

Ce review package exclut volontairement :

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- `local/docs/authoring/`
- les ressources candidates non incluses dans la shortlist

Le but est de concentrer la revue sur la **canonical baseline**, et non sur le bruit historique de l’espace de travail de l’auteur.

