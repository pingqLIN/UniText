# UniText — Projektmodi

> Status: Template Base
> Zweck: Unterscheidet zwischen Authoring-Repo und extern bereitgestelltem Starter-/Template-Modus.

## 1. Zwei Modi

### Lokales Entwicklungsprojekt

Dient dem fortlaufenden Entwickeln, Aufnehmen, Reparieren und Verwalten durch den Autor selbst.

Kann enthalten:

- Inventories
- Backups
- Drift-Logs
- Migrationsartefakte
- plattformspezifische Notizen

### Projekt-Template

Dient dazu, anderen Personen eine eigene `UniText`-Instanz zu ermöglichen.

Soll enthalten:

- logische Verträge
- Kerndokumente
- Minimalbeispiele
- plattformunabhängige Regeln

Soll nicht enthalten:

- lokale absolute Pfade
- persönliche Nutzungsspuren
- Backup-Snapshots
- Drift-Historie
- einzelne Deployment-Defaults

## 2. Faustregel

Wenn ein Inhalt beschreibt:

- `wie UniText funktionieren sollte`
  - dann gehört er eher ins `Project Template`
- `wie ein bestimmter Authoring-Workspace aktuell konfiguriert ist`
  - dann gehört er eher ins `Local Development Project`

## 3. Veröffentlichungsregel

Wenn ein Template veröffentlicht werden soll:

1. Kerndokumente und template-safe examples behalten
2. Local-only state artifacts entfernen
3. Lokale Pfade, Konten und maschinenspezifische Werte entfernen
4. Referenzimplementierungen in abstrakte Beispiele umschreiben
