# UniText — Modes du projet

> Statut : `Template Base`
> Objectif : distinguer le dépôt d’authoring du starter / template publié.

## 1. Two Modes

### Local Development Project

Utilisé par l’auteur pour continuer à développer, gouverner, corriger et maintenir le projet.

Peut contenir :

- inventaires
- backups
- journaux de dérive
- artefacts de migration
- notes spécifiques à une plateforme

### Project Template

Utilisé pour permettre à d’autres personnes d’initialiser leur propre instance de `UniText`.

Doit contenir :

- les contrats logiques
- les documents centraux
- des exemples minimaux
- des règles indépendantes de la plateforme

Ne doit pas contenir :

- des chemins absolus locaux
- des traces d’usage personnel
- des snapshots de sauvegarde
- l’historique de dérive
- des valeurs par défaut propres à un seul déploiement

## 2. Rule Of Thumb

Si un contenu décrit :

- `comment UniText devrait fonctionner`
  - il est plus adapté au `Project Template`
- `comment l’espace de travail de cet auteur est configuré`
  - il est plus adapté à `Local Development Project`

## 3. Publishing Rule

Lors de la publication d’un template :

1. conserver les documents centraux et les exemples `template-safe`
2. retirer les artefacts d’état local uniquement
3. retirer les chemins locaux, comptes et valeurs spécifiques à une machine
4. réécrire l’implémentation de référence sous forme d’exemples abstraits

