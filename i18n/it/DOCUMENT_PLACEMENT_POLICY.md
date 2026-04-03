[English](../../DOCUMENT_PLACEMENT_POLICY.md) | [繁體中文](../zh-TW/DOCUMENT_PLACEMENT_POLICY.md) | [简体中文](../zh-CN/DOCUMENT_PLACEMENT_POLICY.md) | [日本語](../ja/DOCUMENT_PLACEMENT_POLICY.md) | [Deutsch](../de/DOCUMENT_PLACEMENT_POLICY.md) | [Français](../fr/DOCUMENT_PLACEMENT_POLICY.md) | [Español](../es/DOCUMENT_PLACEMENT_POLICY.md) | [한국어](../ko/DOCUMENT_PLACEMENT_POLICY.md) | [Italiano](DOCUMENT_PLACEMENT_POLICY.md)

# UniText — Politica di collocazione dei documenti

> Stato: Active Baseline
> Scopo: definire in quale layer devono vivere i documenti di governance, reference, authoring e operations, così da evitare che shared content e live workspace content finiscano mescolati.

## 1. Purpose

UniText è contemporaneamente:

- un authoring workspace
- una shared registry baseline
- una sorgente di export template / rebuild

Per questo, se si guarda solo al tema del documento, è facile collocarlo nel layer sbagliato.

Questa regola risponde a:

- quali tipi di documenti devono andare in `registry/`
- quali tipi di documenti devono andare in `local/`
- quali tipi di documenti devono andare in `ops/`
- quali documenti possono essere tracked
- quali documenti devono restare solo nello spazio locale di authoring ignorato

## 2. Core Rule

Quando si decide dove collocare un documento, conta prima la natura del contenuto e non l'area tematica.

- se il documento descrive shared canonical truth, va nel shared layer
- se descrive lo stato attuale di un singolo authoring workspace, va nel local layer
- se descrive cronologia operativa, risultati di export, audit evidence o generated state, va nel operations layer

## 3. Placement Matrix

| Content type | Canonical location | Tracked | Share-safe | Notes |
|---|---|---|---|---|
| principi architetturali, regole di governance, spec template-safe | root docs oppure `registry/` | Yes | Yes | devono evitare live workspace values |
| shared sanitized reference | `registry/.../references/` | Yes | Yes | può descrivere la struttura dei campi, ma i valori devono essere redacted o placeholder |
| shared workflow / runbook / template | `registry/workflow/` | Yes | Yes | non deve essere legato a una sola macchina autore |
| machine-local path map / wiring notes | `local/docs/` | Case-by-case | Usually no | location / state sono ammessi, plaintext secret no |
| live workspace baseline | `local/docs/*_WORKSPACE_BASELINE.md` | No | No | deve essere ignorato |
| live operational checklist | `local/docs/*_LIVE.md` | No | No | deve essere ignorato |
| authoring plans / drafts / review notes | `local/docs/authoring/` | No | No | deve essere ignorato |
| generated audit trail / export output / drift report | `ops/` | No | No | è state, non canonical source |

## 4. Naming Rules

Se uno stesso tema richiede sia una versione shared sia una live, per default usa un naming a coppia:

- shared sanitized doc
  - `registry/.../references/<topic>.md`
- live workspace doc
  - `local/docs/<TOPIC>_WORKSPACE_BASELINE.md`
  - oppure `local/docs/<TOPIC>_LIVE.md`

## 5. Pair Rule

Quando shared sanitized doc e live workspace doc esistono insieme, occorre rispettare:

1. la versione shared conserva solo struttura template-safe e redacted placeholder
2. la versione live resta solo in `local/docs/` o `local/docs/authoring/`
3. la versione shared deve indicare dove si trova la versione live
4. la versione live deve a sua volta indicare la shared sanitized reference corrispondente

## 6. Publishing Rule

Queste affermazioni non vanno confuse:

- template export passes
- rebuild export passes
- branch is publish-safe

Il fatto che un export template / rebuild sia pulito significa solo che il pacchetto esportato ha confini più puliti. Non significa che tutto il tracked content del repo di authoring sia sicuro da pushare.

## 7. Quick Decisions

Se non sei sicuro di dove collocare un documento, poni prima queste tre domande:

1. questo documento descrive come appare attualmente un singolo authoring workspace?
   - sì: privilegia `local/docs/`
2. questo documento è un risultato operativo, un artefatto di audit, un pacchetto export o un drift report?
   - sì: privilegia `ops/`
3. questo documento deve poter essere referenziato in modo sicuro da template / rebuild / shared registry?
   - sì: privilegia root docs, `registry/` oppure il shared workflow layer

## 8. Common Misplacements

- mettere una live Cloudflare baseline in `registry/.../references/`
- mettere uno strategy / review plan nella root
- trattare un export output o una audit evidence come canonical reference
- scrivere machine-specific path direttamente nelle shared governance docs

## 9. Review Gate

Prima di aggiungere qualsiasi documento di governance / reference, bisogna almeno verificare:

- che descriva shared truth e non live workspace state
- che, se pushato, resti conforme a `NO_PUBLISH_POLICY.md` e alle aspettative template-safe
- che non serva invece una coppia sanitized/live invece di un singolo file che prova a contenere entrambe

## 10. Related Docs

- `README.md`
- `INDEX.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `NO_PUBLISH_POLICY.md`
