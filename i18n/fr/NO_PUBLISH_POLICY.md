# UniText — Politique de non-publication

> Statut : `Active`
> Objet : définir ce qui ne doit jamais être poussé, téléversé ou publié sans autorisation explicite.

## 1. Règle centrale

Sauf autorisation explicite de l’utilisateur, le contenu suivant ne doit jamais être poussé, téléversé, publié ni synchronisé vers un service réseau :

- `git push`
- les publications sur les plateformes sociales
- les documents cloud
- les services de collage de texte
- toute API tierce ou tout service d’hébergement

## 2. Contenu sensible par défaut

Les éléments suivants sont sensibles par défaut :

- les brouillons de messages sociaux
- les comparaisons ou discussions de collaboration avec d’autres projets
- les notes de revue
- les documents de stratégie, de roadmap ou de planification
- les orientations de conception qui n’ont pas encore été annoncées publiquement

## 3. Standard d’autorisation

Une publication n’est permise que si :

- l’utilisateur a indiqué explicitement que la publication est autorisée
- si seule une partie du contenu est approuvée, seule cette partie peut être publiée
- un `private repo` n’équivaut pas à une permission automatique de publier

## 4. Règle pour les agents

Tous les agents qui travaillent dans ce dépôt doivent respecter les règles suivantes :

1. Ne faites pas de `git push` sans autorisation explicite.
2. Ne postez pas le contenu vers des services externes sans autorisation explicite.
3. Si l’utilisateur autorise seulement la création d’un remote ou d’un dépôt privé, ne supposez jamais que cela autorise aussi le reste du contenu sensible.
4. Si le contenu concerne d’autres projets, des discussions stratégiques ou des brouillons de messages sociaux, appliquez une prudence maximale.

## 5. Sujets explicitement sensibles à ce stade

Les sujets suivants doivent être traités avec une prudence particulière :

- `SOCIAL_POSTS_2026-03-24.md`
- `SKILL0_COLLABORATION_VISION.md`
- toute autre discussion stratégique liée à `skill-0` ou à la revue externe

## 6. Interprétation opérationnelle

Si une publication devient nécessaire, procédez toujours dans cet ordre :

1. confirmer le périmètre autorisé
2. confirmer la destination autorisée
3. exécuter seulement ensuite le `push`, l’`upload` ou le `posting`
