# Local Overlay

Questa cartella contiene **deployment locale, script, mappa dei path e altri overlay non centrali**.

Lo scopo è semplice:

- evitare che la configurazione locale inquini il concetto centrale del repository
- concentrare qui le modifiche specifiche della macchina
- rendere l’intera cartella `local/` eliminabile e ricreabile, se necessario

## Contenuti

- `docs/`
  - note di deployment e documenti di mapping locali
- `scripts/`
  - script eseguibili in locale

## File attuali

- [docs/authoring](/mnt/q/UniText/local/docs/authoring)
  - documenti core potenziati, mantenuti come riferimento prima della rifattorizzazione
- [docs/MCP_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/MCP_DEPLOYMENT_NOTES.md)
  - note attuali di deployment e wiring MCP
- [docs/PATH_MAP.md](/mnt/q/UniText/local/docs/PATH_MAP.md)
  - riferimento ai path di deployment correnti e al confronto storico
- [docs/WORKFLOW_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/WORKFLOW_DEPLOYMENT_NOTES.md)
  - note attuali di wiring del workflow
- [scripts/sync-skills.ps1](/mnt/q/UniText/local/scripts/sync-skills.ps1)
  - script di sync locale

## Regola

Se un contenuto descrive:

- come questo sistema dovrebbe funzionare
  - non dovrebbe stare in `local/`
- come questa istanza è configurata oggi
  - dovrebbe stare in `local/`

