# Adoption Review Checklist

> Status: Aktiv
> Zweck: Definiert die minimale Prüfstufe für den `REVIEW`-Schritt im Adoption-Flow.

## Erforderlich

- [ ] Verzeichnisname folgt der `id`-Regel
- [ ] `SKILL.md` ist vorhanden
- [ ] `SKILL.md` beginnt mit Frontmatter
- [ ] Frontmatter enthält mindestens `name` und `description`
- [ ] `canonical_location` lässt sich sinnvoll auf `/registry/{type}/{id}` abbilden
- [ ] Keine offensichtlichen Defekte, Leerstellen oder abgeschnittenen Inhalte

## Empfohlen

- [ ] Es gibt eine `LICENSE.txt` oder eine gleichwertige Lizenzbeschreibung
- [ ] Es gibt einen klaren Abschnitt `Usage`, `Workflow` oder `Process`
- [ ] Keine hart codierten persönlichen Konten oder lokalen absoluten Pfade
- [ ] Wenn Scripts / References enthalten sind, sind die Pfadbeziehungen klar und für Agents auffindbar

## Review-Ergebnis

- `approve`
  - kann direkt in `DRY-RUN` übergehen
- `needs-fix`
  - Metadaten oder Inhalt zuerst nachbessern
- `hold`
  - es gibt einen Konflikt um die kanonische Quelle oder ein Inhaltsqualitätsproblem; kein Übergang nach `ADOPT`
