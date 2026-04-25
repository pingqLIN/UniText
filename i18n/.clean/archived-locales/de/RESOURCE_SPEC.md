# UniText — Resource Spec

> Status: Template Base
> Geltungsbereich: logische Verträge für Shared Resources, ohne Bindung an ein einzelnes Betriebssystem, Verzeichnislayout oder Speicherformat.

Dieses Spec geht davon aus, dass alle Kern-Metadaten stabil in reinem Text getragen werden können, damit AI und Menschen sie gemeinsam lesen, vergleichen und versionieren können.

## 1. Scope

Dieses Spec gilt für:

- `skills`
- `mcp`
- `agents`
- `workflow`

Es gilt nicht für:

- operations state artifacts
- plattformspezifische Pfadzuordnungen
- interne Ausführungsdetails eines Adapters

## 2. Identity Rules

Die Hauptidentität einer Shared Resource besteht aus der Kombination:

- `type`
- `id`

`id` soll:

- nur Kleinbuchstaben, Ziffern und `-` verwenden
- keine Leerzeichen enthalten
- keine betriebssystemspezifischen Trennzeichen enthalten

## 3. Canonical Location

`canonical_location` muss ein logischer kanonischer Pfad sein und nicht der absolute Pfad eines bestimmten Rechners.

Beispiele:

- `/registry/skills/example-skill`
- `/registry/mcp/example-mcp`
- `/registry/agents/example-agent`

## 4. Metadata Tiers

### Required

- `id`
- `type`
- `canonical_location`
- `status`

### Recommended

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

### Optional

- `owner`
- `provenance`
- `notes`
- `last_verified`

## 5. Lifecycle

Erlaubte `status`-Werte:

- `draft`
- `active`
- `deprecated`
- `archived`

## 6. Defaults

- Wenn `source_of_truth` fehlt, gilt er als identisch mit `canonical_location`
- Wenn `supported_clis` fehlt, gilt er als `undocumented`
- Wenn `delivery_guidance` fehlt, wird er aus Adapter- / Operations-Dokumenten abgeleitet

## 7. Delivery Guidance

`delivery_guidance` ist ein Hinweis für Discovery, kein fest verdrahteter Delivery-Modus.

Er kann beschreiben:

- welche Adapter-Klasse man prüfen sollte
- ob Plattformunterschiede existieren
- ob `OPERATIONS.md` gelesen werden sollte

Er soll nicht festschreiben:

- Plattform-absolute Pfade
- dauerhaft festgelegte Delivery-Modi

## 8. Conflict Rules

Wenn dieselbe `(type, id)`-Kombination zu mehreren Inhaltsvarianten führt:

- nicht automatisch überschreiben
- die kanonische Quelle nicht stillschweigend annehmen
- bei `REVIEW / DRY-RUN` stoppen

Erlaubte Ergebnisse:

- eine kanonische Quelle explizit auswählen
- mit anderer `id` neu benennen
- als `deprecated` oder `archived` markieren
- vorerst als `draft` belassen

## 9. Example

```yaml
id: example-skill
type: skills
canonical_location: /registry/skills/example-skill
status: draft
source_of_truth: /registry/skills/example-skill/SKILL.md
supported_clis: undocumented
delivery_guidance: Use the skills adapter; resolved mode depends on CLI capabilities and local environment.
```
