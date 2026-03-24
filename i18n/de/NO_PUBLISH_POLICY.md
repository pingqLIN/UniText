# UniText — No-Publish-Richtlinie

> Status: Aktiv
> Zweck: Definiert, welche Inhalte ohne ausdrückliche Erlaubnis nicht gepusht, hochgeladen oder gepostet werden dürfen.

## 1. Kernregel

Sofern der Nutzer nicht ausdrücklich autorisiert hat, dürfen die folgenden Inhalte nicht auf irgendeinen Netzwerkdienst gepusht, hochgeladen, gepostet oder synchronisiert werden:

- GitHub-Push
- Beiträge auf Social-Plattformen
- Cloud-Dokumente
- Paste-Dienste
- jede Drittanbieter-API oder Hosting-Services

## 2. Standardmäßig sensible Inhalte

Die folgenden Inhalte gelten standardmäßig als nicht veröffentlichbar:

- Entwürfe für Social Posts
- Vergleiche oder Kollaborationsdiskussionen mit anderen Projekten
- Review-Notizen
- Strategie-, Roadmap- oder Planungsdokumente
- Designrichtungen, die noch nicht öffentlich angekündigt wurden

## 3. Freigabestandard

Veröffentlichung ist nur dann erlaubt, wenn:

- der Nutzer ausdrücklich mitteilt, dass veröffentlicht werden darf
- bei Teilfreigaben nur der freigegebene Teil veröffentlicht wird
- ein `private repo` nicht automatisch als Veröffentlichungsfreigabe gilt

## 4. Agent-Regel

Alle Agents in diesem Repo müssen Folgendes einhalten:

1. Ohne ausdrückliche Erlaubnis kein `git push`
2. Ohne ausdrückliche Erlaubnis keine Inhalte in sozialen Medien oder andere externe Dienste posten
3. Wenn der Nutzer nur das Erstellen eines Remotes oder eines privaten Repos erlaubt, darf daraus nicht automatisch eine Freigabe für andere sensible Inhalte abgeleitet werden
4. Wenn Inhalte andere Projekte, strategische Diskussionen oder Social-Post-Entwürfe betreffen, ist ein noch konservativerer Standard anzuwenden

## 5. Derzeit ausdrücklich sensible Themen

Bis auf Weiteres sollten die folgenden Inhaltstypen besonders vorsichtig behandelt werden:

- `SOCIAL_POSTS_2026-03-24.md`
- `SKILL0_COLLABORATION_VISION.md`
- weitere strategische Diskussionen rund um `skill-0` oder externe Reviews

## 6. Operative Auslegung

Falls künftig veröffentlicht werden soll, empfiehlt sich die Aufteilung in drei Schritte:

1. Erst den Umfang der erlaubten Veröffentlichung bestätigen
2. Dann das Zielsystem oder die Plattform bestätigen
3. Erst danach `push` / `upload` / `posting` ausführen
