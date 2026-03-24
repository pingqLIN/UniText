# Couche Locale

Ce répertoire contient la **couche locale de déploiement, les scripts, les cartes de chemins et les autres éléments de recouvrement non centraux**.

Son objectif est simple :

- éviter que les configurations locales polluent les concepts centraux de la racine
- concentrer la maintenance locale en un seul endroit
- permettre de supprimer puis reconstruire `local/` si nécessaire

## Contenu

- `docs/`
  - notes de déploiement et fichiers de correspondance locaux
- `scripts/`
  - scripts d’exécution locale

## Fichiers actuels

- [docs/authoring](/mnt/q/UniText/local/docs/authoring)
  - documents centraux renforcés conservés avant la refonte
- [docs/MCP_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/MCP_DEPLOYMENT_NOTES.md)
  - explications actuelles du déploiement et du raccordement MCP local
- [docs/PATH_MAP.md](/mnt/q/UniText/local/docs/PATH_MAP.md)
  - référence des chemins de déploiement actuels et comparaison historique
- [docs/WORKFLOW_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/WORKFLOW_DEPLOYMENT_NOTES.md)
  - explications du raccordement workflow local actuel
- [scripts/sync-skills.ps1](/mnt/q/UniText/local/scripts/sync-skills.ps1)
  - script de synchronisation local

## Règle

Si un contenu décrit :

- la manière dont ce système devrait fonctionner
  - il ne doit pas être placé dans `local/`
- la manière dont cette instance est configurée actuellement
  - il doit être placé dans `local/`

