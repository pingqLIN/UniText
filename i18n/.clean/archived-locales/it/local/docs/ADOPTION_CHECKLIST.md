# Adoption Review Checklist

> Stato: Active
> Uso: definire il set minimo di controlli per lo step `REVIEW` dell’adoption flow.

## Obbligatori

- [ ] il nome della cartella rispetta la regola di `id`
- [ ] esiste `SKILL.md`
- [ ] `SKILL.md` inizia con un frontmatter
- [ ] il frontmatter contiene almeno `name` e `description`
- [ ] `canonical_location` può corrispondere in modo ragionevole a `/registry/{type}/{id}`
- [ ] non ci sono contenuti chiaramente rotti, vuoti o troncati

## Raccomandati

- [ ] esiste `LICENSE.txt` o una nota di licenza equivalente
- [ ] esiste una sezione chiara per Usage, Workflow o Process
- [ ] non ci sono account personali o path assoluti locali hardcoded
- [ ] se ci sono script o references, la relazione tra i path è chiara e individuabile dall’agent

## Esito della review

- `approve`
  - può passare direttamente a `DRY-RUN`
- `needs-fix`
  - servono prima metadata aggiuntivi o cleanup del contenuto
- `hold`
  - esiste un conflitto sulla canonical source o un problema di qualità del contenuto; non può passare ad `ADOPT`

