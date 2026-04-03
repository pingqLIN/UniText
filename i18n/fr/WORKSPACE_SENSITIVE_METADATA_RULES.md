[English](../../WORKSPACE_SENSITIVE_METADATA_RULES.md) | [繁體中文](../zh-TW/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [简体中文](../zh-CN/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [日本語](../ja/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Deutsch](../de/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Français](WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Español](../es/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [한국어](../ko/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Italiano](../it/WORKSPACE_SENSITIVE_METADATA_RULES.md)

# Workspace Sensitive Metadata Rules

> Statut : Active Baseline
> Usage : définir les règles de détection, les règles de maintenance et les limites de validation des workspace-sensitive metadata sur les shared surfaces.

## 1. Purpose

`WORKSPACE_SENSITIVE_METADATA_RULES.json` est la source de règles partagée entre l'authoring repo et l'exported starter package. Elle sert à réduire les dérives suivantes :

- des shared docs qui contiennent des chemins absolus locaux
- des shared scripts qui contiennent des live workspace hostnames
- des shared governance files qui contiennent des live redirect URIs ou des Cloudflare IDs
- boundary verify et template verify qui utilisent des jeux de règles différents

Ce document explique :

- ce que signifie chaque section du fichier de règles
- quand il faut ajouter une nouvelle règle
- comment éviter de classer un sanitized placeholder comme live metadata
- quelles validations doivent être relancées après une modification de règle

## 2. Schema

`WORKSPACE_SENSITIVE_METADATA_RULES.json` contient actuellement quatre sections de premier niveau :

- `shared_surface_scope`
  - définit les tracked shared surfaces analysées par défaut par repo-side boundary verify
- `path_rules`
  - définit quels tracked paths ne doivent pas apparaître dans une shared surface
- `content_patterns`
  - définit quels contenus textuels sont considérés comme workspace-sensitive metadata
- `self_test_cases`
  - définit des cas positifs et négatifs intégrés afin d'éviter des régressions silencieuses après modification des regex

## 3. Maintenance Rules

- quand un nouveau shared governance doc ou shared control script est ajouté et qu'il fait partie du repo-side boundary review, il doit aussi être ajouté à `shared_surface_scope`
- quand un nouveau type de live metadata apparaît, il faut d'abord compléter `content_patterns`, puis les `self_test_cases` correspondants
- si un placeholder doit être considéré comme exemple sûr, il faut ajouter un self-test case avec `expected_labels = []`
- si une regex n'apparaît dans un script qu'en tant que chaîne de règle, il faut définir explicitement `skip_script_pattern_lines`
- il ne faut pas ajouter des paths authoring-only ou operations-only à `shared_surface_scope` pour masquer un faux positif ; il faut d'abord vérifier si le document est placé dans la mauvaise couche

## 4. Required Validation

Après chaque modification de `WORKSPACE_SENSITIVE_METADATA_RULES.json`, il faut au minimum relancer :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\validate-workspace-sensitive-metadata-rules.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-workspace-boundaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

Si la modification affecte la starter baseline, il faut aussi relancer :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

## 5. Design Boundary

L'objectif de cet ensemble de règles est :

- de fournir des heuristic controls stables, maintenables et vérifiables sur les shared surfaces

Ce n'est pas :

- un validateur de schéma complet pour tous les types de secret
- un système DLP générique pour tous les infrastructure providers
- un outil de scan exhaustif des zones local-only / ops-only

Si les types de metadata continuent à s'élargir, l'étape suivante doit être d'étendre la source de règles et les cas de test, et non de remettre des live references dans la shared registry.
