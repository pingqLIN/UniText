# Checklist de revue d’adoption

> Statut : `Active`
> Utilité : définir le standard minimal de vérification pour l’étape `REVIEW` du flux d’adoption.

## Obligatoire

- [ ] le nom du dossier respecte la règle `id`
- [ ] `SKILL.md` existe
- [ ] `SKILL.md` commence par un frontmatter
- [ ] le frontmatter contient au minimum `name` et `description`
- [ ] `canonical_location` peut raisonnablement correspondre à `/registry/{type}/{id}`
- [ ] aucun contenu n’est manifestement corrompu, vide ou tronqué

## Recommandé

- [ ] il existe un `LICENSE.txt` ou une notice équivalente
- [ ] il y a une section `Usage`, `Workflow` ou `Process` claire
- [ ] il n’y a aucun compte personnel ni chemin absolu local codé en dur
- [ ] si des scripts / références existent, leurs relations de chemin sont claires et détectables par un agent

## Résultat de la revue

- `approve`
  - peut passer directement à `DRY-RUN`
- `needs-fix`
  - il faut d’abord compléter la metadata ou nettoyer le contenu
- `hold`
  - il existe un conflit de source canonique ou un problème de qualité de contenu, donc impossible de passer à `ADOPT`

