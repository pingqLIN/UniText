# UniText × skill-0 — Kollaborationsvision

> Status: Concept Draft
> Zweck: Definiert die Beziehung zwischen `UniText` und `skill-0`, mögliche Kooperationsräume, Wege und die aktuell fehlenden Mechanismen.

## 1. Executive Summary

`UniText` und `skill-0` sind weder gegeneinander noch redundant, sondern können eine echte Upstream/Downstream-Beziehung bilden:

- `UniText` verantwortet die **Registry / Delivery / Governance** von Shared Resources
- `skill-0` nimmt High-Level-Skills auf, zerlegt und normalisiert sie in ein allgemein nutzbares **Atomic Operation Set**

Darum ist die sinnvollste Zusammenarbeit nicht „wer ersetzt wen“, sondern:

**UniText liefert kanonische Inputs und eine governte Trägerschicht, skill-0 liefert Decomposition-, Normalization- und Recomposition-Fähigkeit.**

## 2. Beide Projekte lösen unterschiedliche Probleme

### UniText

`UniText` löst:

- wie Shared Resources kanonisch gemacht werden
- wie sie zwischen mehreren AI CLIs geliefert werden
- wie Veränderungen mit `SCAN -> REVIEW -> DRY-RUN -> ADOPT -> DELIVER -> VERIFY` gesteuert werden

Also:

**Distribution / Governance Problem**

### skill-0

`skill-0` löst:

- aus welchen kleinsten Operationseinheiten ein High-Level-Skill tatsächlich besteht
- welche Schritte wiederverwendbare Primitives sind
- welche Beschreibungen nur Surface Wording sind und welche die Kernoperationen darstellen
- ob sich ein High-Level-Skill in eine kleinere, allgemeinere und besser portable Fähigkeit zerlegen lässt

Also:

**Abstraction / Compiler / Normalization Problem**

## 3. Beziehung zwischen beiden

Aus Sicht von `skill-0` ist der wichtigste Wert von `UniText` nicht bloß „ein verteilbares Ergebnis“, sondern:

- eine stabile High-Level-Skill-Quelle
- ein kanonisches Korpus mit logischer Identität und Metadaten
- ein Datensatz, der dauerhaft analysier- und vergleichbar bleibt

Die Beziehung lässt sich so beschreiben:

| Projekt | Primäre Rolle |
|---|---|
| `UniText` | kanonische Source of Truth für Shared Resources |
| `skill-0` | Analyzer / Decomposer / Compiler über High-Level-Skills |

Kurz gesagt:

**UniText speichert Skills, skill-0 zerlegt Skills.**

## 4. Aktueller Kooperationsraum

Auch ohne das Kern-Schema von `UniText` zu ändern, gibt es bereits Kooperationsräume:

### 4.1 UniText als Input-Korpus verwenden

`skill-0` kann diese Inhalte direkt als Input verwenden:

- `registry/skills/*/SKILL.md`
- die Katalog-Metadaten in `INDEX.md`
- den Identity- / Canonical-Location-Vertrag aus `RESOURCE_SPEC.md`

So analysiert `skill-0` nicht verstreute Kopien, sondern einen sauberen kanonischen Skill-Korpus.

### 4.2 UniText als governter Staging Ground

Die Analyseausgaben von `skill-0` können vorerst außerhalb des kanonischen Registry liegen und stattdessen in:

- `/operations`
- zum Beispiel `ops/analysis/skill-0/`

Die Vorteile sind:

- das Shared-Resource-Schema wird nicht zu früh verschmutzt
- das Output-Format kann erst einmal stabil beobachtet werden
- `skill-0` wird als Analysis-Pipeline gesehen und nicht sofort als kanonische Quelle

### 4.3 UniText-Review-Flow für abgeleitete Outputs

Wenn `skill-0` Ausgaben erzeugt wie:

- Atom Maps
- normalisierte Schrittmengen
- Shared-Subroutine-Cluster
- Recomposition-Kandidaten

dann können diese Outputs zunächst nach dem Review-Mindset von `UniText` geprüft werden:

- Ist die Identität stabil?
- Ist die Benennung klar?
- Ist die Zuordnung zurück zum Original-Skill nachvollziehbar?
- Braucht es eine menschliche Entscheidung über die kanonische Form?

## 5. Wahrscheinlichste Kooperationsmodi

### Mode A — skill-0 als externer Analyzer

`skill-0` nutzt `UniText` als Datenquelle und erzeugt Analyse-Reports, schreibt aber nicht zurück ins Registry.

Geeignet für:

- schnelle Validierung der Decomposition-Methode
- Skill-Overlap-Analyse
- Suche nach wiederverwendbaren Primitives

Vorteile:

- sehr niedrige Einstiegskosten
- fast keine Schema-Änderungen in `UniText`

Nachteile:

- Ergebnisse bleiben Sidecar-Artefakte
- werden schwerer zu einer gemeinsamen kanonischen Ressource

### Mode B — skill-0 als Sidecar-Generator

`skill-0` liest `registry/skills` und erzeugt angrenzende, maschinenlesbare Sidecars, zum Beispiel:

- `skill.atoms.json`
- `skill.graph.json`
- `skill.coverage.json`

Vorteile:

- klare Zuordnung zwischen Skill und Atom
- tooling-freundlicher als ein reiner Report

Nachteile:

- berührt schneller die Schema-Grenzen von `UniText`
- es muss definiert werden, was kanonisch ist und was nur generiert wurde

### Mode C — Primitives werden ein erstklassiger Ressourcentyp

Wenn die Zusammenarbeit reift, kann `UniText` neue formale Ressourcentypen ergänzen, etwa:

- `/registry/primitives`
- oder `/registry/operations`

Damit wären die Outputs von `skill-0` nicht mehr bloß Analysebeilagen, sondern formal vom Registry verwaltete Shared Resources.

Vorteile:

- eine echte gemeinsame Sprachschicht
- Grundlage für Cross-Skill-Recomposition

Nachteile:

- das Ressourcenmodell von `UniText` muss angepasst werden
- neue Metadaten-Specs, Adoption-Flows und Verifikationsregeln werden nötig

## 6. Was heute fehlt

Derzeit fehlt noch die natürliche tiefe Integration, vor allem wegen dieser Punkte:

### 6.1 Fehlender kanonischer Typ für Primitives

`UniText` hat aktuell nur diese First-Class-Resource-Typen:

- `skills`
- `mcp`
- `agents`
- `workflow`

Es gibt noch keine:

- `primitives`
- `operations`
- `atoms`

Damit gibt es für die eigentlichen Kernoutputs von `skill-0` noch keine erste Stufe im `UniText`-Modell.

### 6.2 Fehlendes Metadaten-Schema für atomare Einheiten

`RESOURCE_SPEC.md` ist gut für High-Level-Shared-Resources, aber noch nicht für:

- atom id
- operation signature
- preconditions / postconditions
- composition rules
- Provenienz zurück zum Quell-Skill

### 6.3 Fehlender Adoption-Flow für abgeleitete Artefakte

`UniText` hat bereits einen Skills-Adoption-Flow, aber noch keinen speziellen Ablauf für:

- denselben Skill, der in unterschiedliche Atom-Sets zerlegt wird
- mehrere Skills, die ähnliche, aber nicht identische Primitives ergeben
- die Frage, wann ein Atom stabil genug ist, um kanonisiert zu werden

### 6.4 Fehlendes Verifikationsmodell

Wenn die Outputs von `skill-0` in eine formellere Phase übergehen sollen, muss mindestens klar sein:

- ist die Decomposition stabil
- ist eine Round-Trip-Recomposition möglich
- verbessert sich das Cross-Skill-Reuse tatsächlich
- oder wurde nur die Beschreibung neu benannt

### 6.5 Fehlende Grenze zwischen Analyse und Kanon

Es fehlt noch eine eindeutige Regel:

- welche `skill-0`-Artefakte nur Analyse sind
- welche bereits als kanonische Shared Resources gelten

Solange diese Grenze unklar bleibt, ist die sicherste Lösung, alles zunächst unter `ops/analysis/skill-0/` zu halten.

## 7. Empfohlene kurzfristige Richtung

Kurzfristig ist der sinnvollste Weg nicht, das Kern-Schema von `UniText` sofort umzubauen, sondern einen schrittweisen Ansatz zu wählen:

**Mode A -> Mode B**

### Phase A — Nur Analyse

Zuerst:

- `registry/skills/*/SKILL.md` als Input verwenden
- Decomposition-Reports erzeugen
- Ergebnisse in `ops/analysis/skill-0/` speichern

Ziel ist hier nicht die Kanonisierung, sondern die Prüfung von:

- stabiler Atom-Extraktion
- sichtbarem Skill-Overlap
- den Primitives, die es wert sind, behalten zu werden

### Phase B — Stabile Sidecars

Wenn das Format stabiler wird:

- Sidecar-Schemas
- Naming Rules
- Source-Skill-Linking
- Baseline-Verifikation

Auch dann ist noch kein neuer Ressourcentyp nötig, aber die Beziehungen

- `skill -> atoms`
- `atom -> source skills`

können bereits klarer aufgebaut werden.

### Phase C — Erstklassige Primitives

Wenn die Analyse ihren Wert gezeigt hat, kann erst dann über folgende Erweiterungen in `UniText` entschieden werden:

- `/registry/primitives`
- `/registry/operations`

Erst an diesem Punkt sollten die folgenden Dateien offiziell angepasst werden:

- `VISION.md`
- `RESOURCE_SPEC.md`
- `INDEX.md`
- `OPERATIONS.md`

## 8. Konkrete erste Deliverables

Für eine erste Zusammenarbeit der beiden Projekte sind diese vier Dinge am wertvollsten:

1. eine `skill-0`-Draft-Schema für Analyse-Outputs definieren
2. 1 bis 2 Skills aus der `Core 8` für Decomposition-Samples auswählen
3. die Outputs unter `ops/analysis/skill-0/` ablegen
4. vergleichen:
   - gemeinsame Atoms zwischen verschiedenen Skills
   - Abstand zwischen Skill-Text und Atom-Ebene
   - ob sich daraus ein nutzbarer Minimal-Workflow rekonstruieren lässt

## 9. Strategische Einordnung

Wenn die Zusammenarbeit gelingt, wird die langfristige Rollenverteilung klar:

- `UniText` wird zum kanonischen Hub für Shared AI Resources
- `skill-0` wird zur Engine für Skill-Normalisierung und Primitive-Extraktion

Als Systemschichten:

| Layer | Projekt |
|---|---|
| Canonical resource governance | `UniText` |
| Skill decomposition / normalization | `skill-0` |
| künftige Primitive-Vocabulary-Schicht | gemeinsames Ergebnis von `UniText × skill-0` |

## 10. Endgültige Position

Die aktuell treffendste Schlussfolgerung ist:

**`UniText` und `skill-0` sind stark verwandt, aber keine doppelte Arbeit.**

Das eine Projekt fokussiert Governance und Delivery, das andere Decomposition und Abstraktion.

Daher ist der kurzfristig sinnvollste Kooperationsweg nicht, `skill-0` direkt in die vorhandenen vier Ressourcentypen von `UniText` zu pressen, sondern:

**`skill-0` zuerst `UniText` als kanonischen Input-Korpus verwenden zu lassen und die Analyseergebnisse zunächst unter `ops/analysis/skill-0/` abzulegen.**

Wenn Output-Format, Nutzen und Verifikationsmethode stabil sind, kann erst danach entschieden werden, ob die Primitive- / Operationsebene offiziell als neuer kanonischer Ressourcentyp aufsteigt.
