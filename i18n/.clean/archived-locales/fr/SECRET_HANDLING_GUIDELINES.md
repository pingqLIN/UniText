# UniText — Directives de gestion des secrets

> Statut : `Draft`  
> Rôle : définir les frontières de stockage, les principes d’opération et la manière de documenter les mots de passe, API keys, tokens et autres données sensibles dans UniText.

## 1. Objectif

Ce document répond aux questions suivantes :

- quelles données comptent comme un secret
- où un secret ne doit pas être stocké
- comment UniText doit enregistrer la « localisation » et l’« état »
- quand un secret peut rester dans une config CLI, et quand il doit passer par un OS secret store ou un helper natif

Ce document ne fournit pas l’implémentation finale d’un produit unique ; il définit les frontières de gouvernance qu’UniText doit respecter.

## 2. Définition d’un secret

Les éléments suivants sont toujours considérés comme `secret` ou `sensitive material` :

- password
- passphrase
- API key
- access token
- refresh token
- session token
- private key
- OAuth client secret
- cookie / session credential
- tout bearer credential pouvant représenter l’identité d’un utilisateur ou d’un système

Les éléments suivants ne sont généralement pas des secrets, mais peuvent rester des métadonnées sensibles :

- endpoint URL
- model name
- provider name
- account email
- état d’un feature toggle
- état `key exists / missing`
- dernière date de mise à jour d’une clé

## 3. Principe de base

Le principe fondamental d’UniText est :

1. `registry/` ne stocke pas de secret
2. `ops/` n’enregistre pas de secret réutilisable
3. `local/` ne peut contenir que des chemins, des adapters et des notes de déploiement, jamais des secrets en clair
4. un vrai secret doit d’abord être stocké dans un OS-level secret store
5. si l’OS secret store n’est pas disponible à court terme, il faut au minimum séparer le secret de la configuration générale

En bref :

- `registry` est une vérité partagée, pas un coffre-fort
- `ops` est une piste d’audit, pas une archive de credentials
- `local` est une couche de câblage, pas un espace de stockage plaintext

## 4. Politique de stockage par couche

| Couche | Peut stocker un secret ? | Recommandation |
|---|---|---|
| `registry/` | Non | ne stocker que les définitions canoniques, le schéma, les hints d’adapter et les métadonnées de ressource |
| `ops/` | Non | ne stocker que des logs redacted, des métadonnées de backup, des drift reports et l’état d’inventaire |
| docs `local/` | Non | peut documenter le type d’emplacement du secret, mais jamais le secret lui-même |
| config CLI | Conditionnel | seulement si le CLI ne supporte qu’un secret basé sur config et si le risque est acceptable |
| OS secret store | Oui | choix prioritaire ; par exemple Windows DPAPI / Credential Manager, macOS Keychain, Linux Secret Service |
| session en mémoire | Oui | acceptable comme matériel runtime temporaire après déchiffrement, mais ne doit pas être l’unique source persistante |

## 5. Modèles approuvés

### 5.1 Meilleur modèle

Adapté aux extensions métier, outils desktop et adapters multi-CLI :

- la configuration non sensible vit dans une config / storage classique
- le secret vit dans l’OS secret store
- le runtime l’injecte en mémoire au démarrage
- l’interface n’affiche que `stored / missing / last updated`, sans remplir de texte clair

### 5.2 Repli acceptable

S’il n’existe pas encore d’intégration avec un OS secret store :

- chaque provider / account stocke ses secrets séparément
- le secret reste séparé de la configuration normale
- le content script / renderer / contexte non fiable ne peut pas le lire directement
- l’audit et l’export ne montrent qu’un état redacted
- le modèle doit être signalé comme `interim storage model`

### 5.3 Inacceptable

Les pratiques suivantes ne doivent pas être considérées comme conformes :

- écrire une API key dans `registry/`
- écrire un token dans `ops/history/`
- coller un exemple de clé complète dans une note de déploiement
- mélanger secrets et configuration générale sans redaction
- emballer les vraies clés dans un review package ou un template package

## 6. Règles de consignation de localisation

La documentation peut indiquer « dans quelle couche se trouve le secret », mais jamais la valeur du secret.

Exemples autorisés :

- `Windows Credential Manager`
- `DPAPI-protected local secret file`
- valeurs non secrètes dans `%USERPROFILE%\\.codex\\config.toml`
- `chrome.storage.local` seulement pour les settings non sensibles du provider
- `chrome.storage.session` pour du matériel runtime de courte durée

Exemples interdits :

- token complet
- API key complète
- Authorization header complet
- valeur de cookie directement réutilisable

## 7. Règles de documentation

Quand un document doit parler de gestion des secrets, il doit respecter :

1. ne documenter que la classe de stockage, pas la valeur réelle
2. ne montrer que des exemples redacted
3. si un exemple est indispensable, utiliser des faux clairs, par exemple :

```text
OPENAI_API_KEY=sk-example-redacted
Authorization: Bearer token-example-redacted
```

4. si un système ne peut actuellement fonctionner qu’avec un modèle plus faible, le document doit préciser :
   - qu’il s’agit d’une solution temporaire
   - quel est le risque connu
   - quelle est la trajectoire d’amélioration

## 8. Règles d’audit et d’export

Tout review package, template package, export d’inventaire ou snapshot `ops` doit :

- supprimer les valeurs secrètes
- supprimer les credentials réutilisables
- conserver seulement l’état redacted nécessaire

Peuvent être conservés :

- provider name
- endpoint
- key exists / missing
- scope ou label de la clé
- last rotated at
- type de backend de stockage

## 9. Échelle de recommandation

L’ordre de priorité recommandé par UniText pour le stockage des secrets est :

1. `OS secret store`
   - Windows : DPAPI / Credential Manager
   - macOS : Keychain
   - Linux : Secret Service / keyring
2. `native helper / native messaging host`
   - quand le CLI ou l’extension ne peut pas persister un secret de façon sûre
3. `separated local secret store`
   - séparé de la config générale et inaccessible directement aux contexts non fiables
4. `runtime session only`
   - utile comme aide, mais ne doit pas être la seule stratégie persistante

## 10. Checklist minimale

Avant d’ajouter dans UniText une ressource ou un adapter qui gère des secrets, vérifiez au minimum :

- le secret est-il exclu de `registry/`
- le secret est-il exclu de `ops/`
- le document n’enregistre-t-il que la localisation / l’état, et jamais la valeur
- l’export / review package applique-t-il bien la redaction
- le backend de stockage actuel est-il documenté
- la trajectoire d’amélioration est-elle documentée

## 11. Guidance pratique pour les browser extensions

Dans un scénario de type browser extension :

- les settings du provider peuvent vivre dans l’extension local storage
- l’API key ne doit pas être mélangée aux settings généraux du provider dans une seule valeur partagée
- chaque provider doit avoir son propre secret
- l’UI doit supporter un état de brouillon staged ; elle ne doit pas perdre la clé à cause d’un switch de provider ou d’un hover / collapse
- pour atteindre un niveau de sécurité supérieur, il faut préférer un native host + OS secret store plutôt que la seule extension storage

## 12. Position actuelle d’UniText

À ce stade, la position officielle d’UniText sur la gestion des secrets est :

- le canonical registry ne porte pas de secret
- la couche locale peut documenter le backend secret et le type de chemin
- les artefacts d’operations doivent être redacted
- si une intégration n’est pas encore reliée à un OS secret store, le document doit le signaler explicitement comme `interim model`

Ce document doit être considéré comme :

- une guidance d’authoring
- une référence de checklist pour la revue
- une ligne de base pour les futures intégrations adapter / secret-store

