# UniText — Richtlinien zum Umgang mit Secrets

> Status: Draft  
> Rolle: Definiert die Speichergrenzen, Betriebsregeln und Dokumentationsform für Passwörter, API Keys, Tokens und andere sensitive Materialien in UniText.

## 1. Zweck

Dieses Dokument beantwortet:

- welche Daten als Secret gelten
- wo Secrets nicht abgelegt werden sollen
- wie UniText „Ort“ und „Status“ dokumentieren sollte
- wann ein CLI-Konfigurationsspeicher ausreicht und wann stattdessen ein OS Secret Store oder ein nativer Helper nötig ist

Dieses Dokument liefert keine finale Implementierung für ein einzelnes Produkt; es definiert die Governance-Grenzen, die UniText einhalten soll.

## 2. Secret-Definition

Folgende Inhalte gelten stets als `secret` oder `sensitive material`:

- Passwort
- Passphrase
- API Key
- Access Token
- Refresh Token
- Session Token
- Private Key
- OAuth Client Secret
- Cookie / Session Credential
- jedes Bearer Credential, das die Identität eines Nutzers oder Systems repräsentiert

Folgende Inhalte sind normalerweise kein Secret, können aber sensible Metadaten sein:

- Endpoint-URL
- Modellname
- Provider-Name
- Account-E-Mail
- Feature-Toggle-Status
- Status `key exists / missing`
- Zeitpunkt der letzten Aktualisierung eines Keys

## 3. Kernprinzip

Das Grundprinzip von UniText lautet:

1. `registry/` speichert keine Secrets
2. `ops/` protokolliert keine wiederverwendbaren Secrets
3. `local/` darf nur Pfad-, Adapter- und Deployment-Notizen enthalten, aber keine Klartext-Secrets
4. Echte Secrets sollen bevorzugt im OS-level Secret Store liegen
5. Falls ein OS Secret Store kurzfristig nicht möglich ist, müssen Secrets mindestens von allgemeinen Einstellungen getrennt bleiben

Kurz gesagt:

- `registry` ist eine Shared Truth, kein Secret Vault
- `ops` ist ein Audit Trail, kein Credential Archive
- `local` ist ein Wiring Overlay, kein Plaintext-Stash

## 4. Speicherpolitik nach Schicht

| Schicht | Darf Secret speichern? | Hinweis |
|---|---|---|
| `registry/` | Nein | nur kanonische Definitionen, Schemas, Adapter-Hinweise und Ressourcen-Metadaten |
| `ops/` | Nein | nur redigierte Logs, Backup-Metadaten, Drift-Reports und Inventory-Status |
| `local/` docs | Nein | darf Secret-Standorttypen dokumentieren, aber nicht den Secret-Wert |
| CLI config | Bedingt | nur wenn die CLI Secrets ausschließlich konfigurationsbasiert unterstützt und das Risiko vertretbar ist |
| OS secret store | Ja | bevorzugt; z. B. Windows DPAPI / Credential Manager, macOS Keychain, Linux Secret Service |
| In-Memory-Session | Ja | als kurzlebiges Runtime-Material akzeptabel, aber nicht als einzige persistente Quelle |

## 5. Freigegebene Muster

### 5.1 Bestes Muster

Geeignet für kommerzielle Erweiterungen, Desktop-Tools und Cross-CLI-Adapter:

- nicht-sensitive Einstellungen liegen in normalem Config / Storage
- Secrets liegen im OS Secret Store
- zur Laufzeit werden sie in den Prozessspeicher injiziert
- die UI zeigt nur `stored / missing / last updated`, nicht den Klartext

### 5.2 Akzeptabler Fallback

Wenn noch keine OS-Secret-Store-Integration verfügbar ist:

- Secret pro Provider / Account getrennt speichern
- Secret und normale Einstellungen trennen
- Content Script / Renderer / untrusted context darf nicht direkt lesen
- Audit und Export zeigen nur den redigierten Status
- in der Dokumentation als `interim storage model` markieren

### 5.3 Nicht akzeptabel

Folgende Vorgehensweisen gelten nicht als passend für UniText:

- API Keys in `registry/` schreiben
- Tokens in `ops/history/` schreiben
- vollständige Key-Beispiele in Deployment-Notizen einfügen
- Secret und normale Einstellungen ohne Redaction zusammen speichern
- echte Keys in Review Packages oder Template Packages mit verpacken

## 6. Regeln für die Dokumentation des Speicherorts

Dokumente dürfen beschreiben, in welcher Schicht ein Secret liegt, aber nicht den Secret-Wert selbst.

Erlaubte Beispiele:

- `Windows Credential Manager`
- `DPAPI-protected local secret file`
- `%USERPROFILE%\\.codex\\config.toml` für nicht-sensitive Einstellungen
- `chrome.storage.local` nur für nicht-sensitive Provider-Einstellungen
- `chrome.storage.session` für kurzlebiges Runtime-Material

Nicht erlaubt:

- vollständiger Token
- vollständiger API Key
- vollständiger Authorization Header
- Cookie-Wert, der direkt wiederverwendbar ist

## 7. Dokumentationsregeln

Wenn ein Dokument Secret Handling erwähnen muss, gilt:

1. Nur die Storage-Klasse dokumentieren, nicht den tatsächlichen Wert
2. Nur redigierte Beispiele verwenden
3. Wenn Beispiele unvermeidlich sind, explizite Platzhalterwerte nutzen, z. B.:

```text
OPENAI_API_KEY=sk-example-redacted
Authorization: Bearer token-example-redacted
```

4. Wenn ein System momentan nur in einem schwächeren Modus funktioniert, muss das Dokument klar markieren:
   - dass es sich um eine Übergangslösung handelt
   - welches bekannte Risiko besteht
   - welcher Upgrade-Pfad vorgesehen ist

## 8. Regeln für Audit und Export

Jedes Review Package, Template Package, Inventory-Export oder Ops-Snapshot muss:

- Secret-Werte entfernen
- wiederverwendbare Credentials entfernen
- den nötigen redigierten Status beibehalten

Erlaubt zu behalten:

- Provider-Name
- Endpoint
- `key exists / missing`
- Key-Scope oder Label
- Zeitpunkt der letzten Rotation
- Typ des Storage-Backends

## 9. Empfehlungshierarchie

Die empfohlene Reihenfolge für Secret Storage ist:

1. `OS secret store`
   - Windows: DPAPI / Credential Manager
   - macOS: Keychain
   - Linux: Secret Service / keyring
2. `native helper / native messaging host`
   - wenn eine CLI oder Extension Secrets nicht sicher direkt persistieren kann
3. `separated local secret store`
   - getrennt von normalem Config-Storage und für untrusted contexts nicht direkt lesbar
4. `runtime session only`
   - nur unterstützend, nie die einzige dauerhafte Strategie

## 10. Minimal-Checkliste

Bevor in UniText irgendeine neue Ressource oder ein Adapter hinzugefügt wird, der Secrets verarbeitet, mindestens prüfen:

- ist das Secret aus `registry/` ausgeschlossen
- ist das Secret aus `ops/` ausgeschlossen
- dokumentiert das Dokument nur Ort / Status und nicht den Wert
- hat der Export / das Review Package Redaction
- ist das aktuell verwendete Storage-Backend dokumentiert
- ist der Upgrade-Pfad dokumentiert

## 11. Praktische Hinweise für Browser-Extensions

Am Beispiel einer Browser Extension:

- Provider-Einstellungen dürfen im Extension-Local-Storage liegen
- der API Key sollte nicht zusammen mit normalen Provider-Einstellungen als ein gemeinsamer Wert gespeichert werden
- jeder Provider sollte sein eigenes Secret haben
- die UI sollte staged drafts unterstützen und nicht durch Provider-Wechsel oder Hover/Collapse Keys verlieren
- für ein höheres Sicherheitsniveau sollte auf native host + OS Secret Store gewechselt werden, statt nur Extension Storage zu nutzen

## 12. Aktuelle Position von UniText

Der offizielle Stand von UniText zum Thema Secret Handling ist derzeit:

- das kanonische Registry trägt keine Secrets
- das lokale Overlay darf Secret-Backend und Pfadtypen dokumentieren
- Operations-Artefakte müssen redigiert sein
- wenn eine Integration noch nicht an den OS Secret Store angebunden ist, muss das Dokument sie ausdrücklich als `interim model` kennzeichnen

Dieses Dokument ist zu verstehen als:

- Authoring-Guidance
- Review-Checklisten-Referenz
- Ausgangsbasis für zukünftige Adapter- / Secret-Store-Integrationen
