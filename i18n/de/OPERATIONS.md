# UniText — Operations

> Status: Template Base
> Rolle: Definiert die Verantwortlichkeiten der Adapter- / Operations-Control-Plane, Delivery-Regeln und Sicherheitsgrenzen.

Alle Delivery- und Mutationsvorgänge sollen `UniText`-Text-Registry- / Spec-Verträge als Source of Truth verwenden.

Wenn eine Operation `password`, `API key`, `token`, `credential` oder andere sensible Materialien betrifft, sind zusätzlich die `SECRET_HANDLING_GUIDELINES.md` zu beachten.

## 1. Scope

Dieses Dokument umfasst:

- Adapter-Verantwortlichkeiten
- Delivery-Modi
- Delivery-Triggers
- Adoption-Flow
- Drift / Repair
- logische zu physische Zuordnung

Dieses Dokument umfasst nicht:

- das Metadaten-Schema für Shared Resources
- die einzige Implementierung einer einzelnen Plattform
- den historischen Zustand eines lokalen Authoring-Repos

## 2. Delivery Modes

| Modus | Wann er verwendet wird |
|---|---|
| `pointer` | für Discovery oder Ressourcen ohne lokale Maschinenregistrierung |
| `mirror` | wenn eine CLI eine lokale Kopie benötigt oder Symlinks unzuverlässig sind |
| `symlink` | wenn eine CLI einen festen Pfad braucht und die Umgebung stabile Links unterstützt |
| `native-config` | wenn eine CLI einen offiziellen Konfigurationspunkt zur Registrierung von Ressourcen besitzt |

Der `delivery mode` wird vom Adapter während der Operation aufgelöst und ist keine feste Eigenschaft der Ressource.

## 3. Delivery Resolution Rules

Der Adapter soll in dieser Priorität entscheiden:

1. Gibt es einen offiziellen Konfigurationspunkt, ist `native-config` bevorzugt
2. Wird ein fester Pfad benötigt und unterstützt die Plattform stabile Links, dann `symlink`
3. Kann ein Symlink nicht sicher verwendet werden, dann `mirror`
4. Dient die Ressource hauptsächlich Discovery oder einem Einstiegspunkt, dann `pointer`

## 4. Delivery Triggers

Delivery darf nur durch explizite Trigger gestartet werden:

- `bootstrap`
- `sync`
- `adopt`
- `repair`

## 5. Safety Rules

### Dry-Run First

Die folgenden Operationen sollen zuerst einen Dry-Run-Plan erzeugen:

- `adopt`
- `repair`
- `sync`, wenn vorhandener Zustand überschrieben wird

### Backup Before Mutation

Alle destruktiven Operationen sollen Folgendes besitzen:

- Backup oder einen gleichwertigen Wiederherstellungspunkt
- nachvollziehbares Operations-Logging
- eine Stop-Bedingung bei Fehlern

### No Silent Canonicalization

Wenn gleichnamige Ressourcen mit unterschiedlichem Inhalt auftreten:

- bei Review stoppen
- der Operator muss die kanonische Quelle explizit bestimmen

## 6. Adoption Flow

1. `SCAN`
   - Kandidatenquellen scannen und alle Ressourcen samt Readiness-Status auflisten
2. `REVIEW`
   - Metadaten, Inhaltsqualität und die Legitimität der kanonischen Quelle anhand der Review-Checkliste prüfen
3. `DRY-RUN`
   - Vorschau darauf, welche Ziele sich durch Adopt oder Delivery ändern würden und ob ein Backup nötig ist
4. `ADOPT`
   - Quellinhalt an die kanonische `registry`-Position schreiben; falls bestehender Inhalt überschrieben wird, zuerst Backup erstellen
5. `DELIVER`
   - Die Adapter liefern den Registry-Inhalt an die passende CLI aus; wenn dabei vorhandener Zustand überschrieben wird, Log und Backup behalten
   - Wenn die CLI `native-config` unterstützt, kann während `bootstrap` eine maschinenlokale Config geschrieben werden; die kanonische Definition bleibt trotzdem in `registry/`
6. `VERIFY`
   - Dateiexistenz, Pfadauflösung, Delivery-Modus und die Ladebedingungen der Ziel-CLI prüfen

## 6.1 First-Run Baseline

Wenn das Ziel ist, dass neue Template-Nutzer auf macOS / Linux / Windows den Minimal-Start schaffen, sollen mindestens vorhanden sein:

- ein plattformübergreifendes `bootstrap`
- ein plattformübergreifendes `verify`
- ein portabler Repo-Backup-Pfad
- ein ausführbares minimales MCP-Baseline-Element

## 7. Operations State

Die folgenden Inhalte gehören zu Operations State und nicht zu Shared Resources:

- Inventories
- Baselines
- Backups
- Drift-Reports
- Repair-Pläne
- Audit-Trails

Sie sollen unter `/operations` liegen und nicht mit `/registry` vermischt werden.

## 8. Logical-to-Physical Mapping

Logische Pfade sind ein stabiler Vertrag; physische Pfade sind deployment-spezifische Zuordnungen.

| Logischer Bereich | Bedeutung | Beispiele für physische Zuordnung |
|---|---|---|
| `/registry/skills` | kanonische Skill-Quellen | gemeinsames Verzeichnis, Repo-Subdir, eingebundener Pfad |
| `/registry/mcp` | kanonische MCP-Definitionen | Konfigurationsordner, generierter Manifest-Root |
| `/registry/agents` | kanonische Agent-Instruktionswurzeln | Agent-Profile-Verzeichnis, gemeinsame Prompt-Bibliothek |
| `/registry/workflow` | Workflow-Dokumente / Runbooks | Workflow-Ordner, projektlokale Docs |
| `/operations` | Inventories, Backups, Drift-Logs | ops-Ordner, State Store, Audit-Verzeichnis |
