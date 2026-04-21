# UniText — Template Release Checklist

> Zweck: Schnelle Prüfung, ob die minimale Bereinigung vor dem Export oder der Veröffentlichung eines Template Packages abgeschlossen ist.

## 1. Docs

- [ ] `README.md` benötigt kein persönliches Vorwissen des Autors zum Verständnis
- [ ] `INDEX.md` kann als Discovery-Einstieg dienen
- [ ] `PROJECT_MODES.md` unterscheidet klar zwischen Template und Authoring Workspace
- [ ] `SECRET_HANDLING_GUIDELINES.md` definiert die Secret-Grenzen und enthält keine echten Credentials
- [ ] `TEMPLATE_RELEASE_PACKAGE.md` ist aktualisiert
- [ ] `MILESTONES.md` spiegelt den aktuellen Phasenstatus wider

## 2. Cleanup Boundaries

- [ ] das Template Package enthält kein `backup/`
- [ ] das Template Package enthält keine `recovered_*`
- [ ] das Template Package enthält keine `.bak_*`
- [ ] das Template Package enthält kein `ops/history/`
- [ ] das Template Package enthält keine review-only docs
- [ ] das Template Package enthält keine maschinenspezifischen absoluten Pfade

## 3. Examples

- [ ] mindestens 1 generic skill example
- [ ] mindestens 1 generic agent example
- [ ] mindestens 1 generic mcp example
- [ ] mindestens 1 generic workflow example
- [ ] mindestens 1 generic local overlay skeleton
- [ ] das Starter Package enthält einen Cross-Platform-`bootstrap -> verify`-Pfad

## 4. Validation

- [ ] `health-check.ps1` besteht
- [ ] `export-template-package.ps1 -DryRun` listet den Package-Inhalt auf
- [ ] `export-template-package.ps1` kann das Package erfolgreich erzeugen
- [ ] `verify-template-package.ps1` besteht
- [ ] `bootstrap.py --dry-run` kann in einer sauberen Umgebung den Initialisierungsinhalt vorschauen
- [ ] `verify-bootstrap.py` kann das First-Run-Wiring verifizieren
- [ ] das Package enthält `manifest.json`
- [ ] das Package enthält `release.json`

## 5. Release Call

Wenn alle Punkte erfüllt sind, gilt:

**geeignet, als template release candidate betrachtet zu werden**

Wenn lokale-only Grenzen noch unklar sind, Beispiele unvollständig sind oder die CLI-Verifikation noch nicht breit genug ist, dann gilt weiterhin:

**template release cleanup baseline**
