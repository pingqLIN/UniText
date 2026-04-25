# UniText — Checklist de release du template

> Utilité : vérifier rapidement qu’un minimum de nettoyage est prêt avant d’exporter ou de publier un template package.

## 1. Docs

- [ ] `README.md` ne dépend pas du contexte personnel de l’auteur pour être compris
- [ ] `INDEX.md` peut servir de point d’entrée pour la discovery
- [ ] `PROJECT_MODES.md` distingue clairement le template du workspace d’authoring
- [ ] `SECRET_HANDLING_GUIDELINES.md` définit la frontière des secrets sans contenir de vraies credentials
- [ ] `TEMPLATE_RELEASE_PACKAGE.md` a été mis à jour
- [ ] `MILESTONES.md` reflète l’état actuel des phases

## 2. Frontières de nettoyage

- [ ] le template package ne contient pas `backup/`
- [ ] le template package ne contient pas `recovered_*`
- [ ] le template package ne contient pas `.bak_*`
- [ ] le template package ne contient pas `ops/history/`
- [ ] le template package ne contient pas de docs réservés à la revue
- [ ] le template package ne contient pas de chemins absolus propres à une machine

## 3. Exemples

- [ ] au moins 1 generic skill example
- [ ] au moins 1 generic agent example
- [ ] au moins 1 generic mcp example
- [ ] au moins 1 generic workflow example
- [ ] au moins 1 generic local overlay skeleton
- [ ] le starter package contient un chemin multiplateforme `bootstrap -> verify`

## 4. Validation

- [ ] `health-check.ps1` passe
- [ ] `export-template-package.ps1 -DryRun` liste le contenu du package
- [ ] `export-template-package.ps1` produit le package avec succès
- [ ] `verify-template-package.ps1` passe
- [ ] `bootstrap.py --dry-run` prévisualise l’initialisation dans un environnement propre
- [ ] `verify-bootstrap.py` valide le first-run wiring
- [ ] le package contient `manifest.json`
- [ ] le package contient `release.json`

## 5. Décision de release

Si tous les points ci-dessus sont validés, on peut considérer que le projet est :

**adapté pour être vu comme un template release candidate**

S’il reste des frontières local-only floues, des exemples incomplets ou une validation CLI insuffisante, il faut encore le considérer comme :

**template release cleanup baseline**

