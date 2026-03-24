# UniText — Specifica delle Risorse

> Stato: Template Base
> Ambito: contratto logico per le shared resources, senza vincoli su un singolo sistema operativo, struttura di cartelle o formato di archiviazione.

Questa specifica assume che tutti i metadata fondamentali possano essere rappresentati in modo stabile in testo puro, così da essere leggibili e confrontabili da persone e AI.

## 1. Ambito

La specifica si applica a:

- `skills`
- `mcp`
- `agents`
- `workflow`

Non si applica a:

- operations state artifacts
- mapping di path specifici della piattaforma
- dettagli interni di esecuzione degli adapter

## 2. Regole di identità

L’identità principale di una shared resource è data dalla combinazione di:

- `type`
- `id`

`id` deve:

- usare lettere minuscole, numeri e `-`
- non contenere spazi
- non contenere separatori specifici del sistema operativo

## 3. Canonical location

`canonical_location` deve essere un logical canonical path, non un path assoluto di una macchina specifica.

Esempi:

- `/registry/skills/example-skill`
- `/registry/mcp/example-mcp`
- `/registry/agents/example-agent`

## 4. Livelli di metadata

### Obbligatori

- `id`
- `type`
- `canonical_location`
- `status`

### Raccomandati

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

### Opzionali

- `owner`
- `provenance`
- `notes`
- `last_verified`

## 5. Ciclo di vita

`status` ammessi:

- `draft`
- `active`
- `deprecated`
- `archived`

## 6. Valori di default

- se manca `source_of_truth`, si intende uguale a `canonical_location`
- se manca `supported_clis`, si intende `undocumented`
- se manca `delivery_guidance`, viene dedotto da adapter / operations

## 7. Delivery guidance

`delivery_guidance` è un suggerimento di discovery, non un delivery mode fisso.

Può indicare:

- quale tipo di adapter consultare
- se esistono differenze di piattaforma
- se è necessario leggere `OPERATIONS.md`

Non dovrebbe fissare:

- path assoluti di piattaforma
- delivery mode permanente e immutabile

## 8. Regole di conflitto

Se la stessa coppia `(type, id)` corrisponde a candidate resources con contenuti diversi:

- non sovrascrivere automaticamente
- non assumere in silenzio la canonical source
- fermarsi in `REVIEW / DRY-RUN`

Risultati ammessi:

- scegliere in modo esplicito la canonical source
- rinominare con un `id` diverso
- marcare come `deprecated` o `archived`
- lasciare temporaneamente `draft`

## 9. Esempio

```yaml
id: example-skill
type: skills
canonical_location: /registry/skills/example-skill
status: draft
source_of_truth: /registry/skills/example-skill/SKILL.md
supported_clis: undocumented
delivery_guidance: Use the skills adapter; resolved mode depends on CLI capabilities and local environment.
```

