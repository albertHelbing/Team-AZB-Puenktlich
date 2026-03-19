# User Stories – *Pünktlich.*

## Shared Definition of Done (DoD)

All user stories in this backlog reference the following shared Definition of Done:

- [ ] Code is written and peer-reviewed
- [ ] Unit tests are written and pass
- [ ] Integration tests are written and pass
- [ ] Code is merged into the main branch
- [ ] UI/UX is consistent with design guidelines
- [ ] Documentation (inline + user-facing) is updated
- [ ] User Acceptance Testing (UAT) is completed
- [ ] Feature is deployed to the staging environment
- [ ] Performance and security testing are completed
- [ ] Product Owner has accepted the story

---

## Shared Definition of Ready (DoR)

A user story is ready to be worked on when:

- Acceptance criteria are defined and agreed upon
- Effort estimate in story points is assigned
- Dependencies on other stories are identified

---

## Effort Estimation Key

| Story Points | Effort |
|---|---|
| 1 | Trivial (< 2 h) |
| 2 | Small (half a day) |
| 3 | Medium (1–2 days) |
| 5 | Large (3–5 days) |
| 8 | Extra Large (1–2 weeks) |

---

## User Stories

---

### US-01 · Kalenderintegration

**Als** Nutzerin
**möchte ich** meinen bestehenden Kalender (Google Calendar, Outlook, Apple Calendar) mit der App verbinden,
**damit** meine Termine automatisch von *Pünktlich.* ausgelesen werden, ohne dass ich sie manuell eingeben muss.

*Abgeleitet aus: Anna – Szenario 1 & 2; Lukas – Szenario 1 & 2; Michael – Szenario 1*

**Aufwandsschätzung:** 5 SP

**Akzeptanzkriterien:**
- Die App bietet eine OAuth-Verbindung für Google Calendar, Microsoft Outlook und Apple Calendar an.
- Nach der Autorisierung werden alle bevorstehenden Termine (mindestens die nächsten 7 Tage) importiert und in der App angezeigt.
- Die Nutzer:in erhält eine Bestätigung, sobald der Kalender erfolgreich verbunden ist.
- Bei einem Verbindungsfehler zeigt die App eine verständliche Fehlermeldung mit Wiederholungsoption.
- Der Kalender kann jederzeit in den Einstellungen getrennt werden.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-02 · Automatische Weckzeitberechnung

**Als** Nutzer
**möchte ich**, dass *Pünktlich.* meine Weckzeit automatisch anhand meines nächsten Termins berechnet,
**damit** ich den Wecker nicht mehr manuell setzen muss.

*Abgeleitet aus: Michael – Szenario 1; Anna – Szenario 1 & 3; Lukas – Szenario 2*

**Aufwandsschätzung:** 5 SP

**Akzeptanzkriterien:**
- Die App berechnet die Weckzeit als: Terminbeginn − Fahrtzeit − Pufferzeit − persönliche Vorbereitungszeit.
- Die berechnete Weckzeit wird am Vorabend mit einer kurzen Erklärung angezeigt (z. B. „25 Min Fahrt + 10 Min Vorbereitung → Weckzeit 04:35").
- Die Nutzer:in kann die vorgeschlagene Weckzeit akzeptieren, anpassen oder ablehnen.
- Wenn kein Termin für den nächsten Tag erkannt wird, wird kein automatischer Alarm erstellt.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-03 · Konfigurierbare Vorbereitungs- und Pufferzeit

**Als** Nutzer
**möchte ich** meine individuelle Vorbereitungszeit am Morgen sowie einen Ankunftspuffer (z. B. für Parkplatzsuche oder Sicherheitsschleusen) festlegen,
**damit** die berechnete Weckzeit meiner realen Routine entspricht.

*Abgeleitet aus: Michael – Szenario 1 (10 Min Umkleide, 10 Min Parkplatzsuche, 5 Min Tor-Puffer); Lukas – Szenario 1 (15 Min Fertigmachen)*

**Aufwandsschätzung:** 2 SP

**Akzeptanzkriterien:**
- Die Nutzer:in kann eine Standard-Vorbereitungszeit (in Minuten) im Profil hinterlegen.
- Die Nutzer:in kann einen globalen Ankunftspuffer (0–60 Min) festlegen sowie Voreinstellungen wählen (z. B. „Werk/Fabrik", „Flughafen", „Uni").
- Beide Werte fließen in jede Alarmberechnung ein und werden in der Alarmzusammenfassung angezeigt.
- Einzelne Events können mit abweichenden Werten überschrieben werden.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-04 · Fahrzeitberechnung mit Verkehrsdaten

**Als** Nutzerin
**möchte ich**, dass die App meine Fahrtzeit per Auto oder ÖPNV unter Berücksichtigung der aktuellen Verkehrslage berechnet,
**damit** mein Alarm die tatsächliche Reisezeit widerspiegelt.

*Abgeleitet aus: Michael – Szenario 1 (25 Min Fahrt, B464); Anna – Szenario 1 (30 Min zum Flughafen); Lukas – Szenario 2 (35 Min U-Bahn)*

**Aufwandsschätzung:** 5 SP

**Akzeptanzkriterien:**
- Die App berechnet die Fahrtzeit per Auto (mit prädiktiven Verkehrsdaten zum geplanten Abfahrtszeitpunkt) sowie per ÖPNV (inkl. Umstiegs- und Fußwegzeiten).
- Die Nutzer:in kann im Profil ein Standard-Verkehrsmittel festlegen und dieses pro Termin überschreiben.
- Die geschätzte Fahrtzeit wird in der Alarmzusammenfassung angezeigt.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-05 · Dynamische Alarmverschiebung bei Verkehrsstörungen

**Als** Nutzer
**möchte ich** automatisch benachrichtigt werden und meinen Alarm früher gestellt bekommen, wenn eine Störung auf meiner geplanten Route gemeldet wird,
**damit** ich trotz unvorhergesehener Verzögerungen pünktlich ankomme.

*Abgeleitet aus: Michael – Szenario 1 („Unfall auf B464 – Abfahrt 04:45"); Lukas – Szenario 2 (Baustelle, 10 Min Verzögerung)*

**Aufwandsschätzung:** 8 SP

**Akzeptanzkriterien:**
- Die App prüft die Verkehrslage am Morgen des Termins (mindestens 60 Min vor dem ursprünglichen Alarm).
- Bei einer erkannten Verzögerung von ≥ 10 Minuten wird der Alarm entsprechend vorverlegt.
- Die Nutzer:in erhält eine Push-Benachrichtigung mit Grund und neuer Alarmzeit (z. B. „Unfall auf B464 – Alarm auf 04:45 verschoben").
- Die Nutzer:in kann die neue Zeit akzeptieren oder zum ursprünglichen Alarm zurückkehren.
- Anpassungen werden nie still und ohne Benachrichtigung vorgenommen.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-06 · Standortbasierte Routenanpassung

**Als** Nutzer
**möchte ich**, dass die App erkennt, wenn ich an einem ungewohnten Ort schlafe, und meine Route von dort neu berechnet,
**damit** mein Alarm auch dann korrekt ist, wenn ich nicht zu Hause bin.

*Abgeleitet aus: Lukas – Szenario 1 (schläft bei einem Freund); Lukas – Szenario 3 (App prüft nachts den Standort)*

**Aufwandsschätzung:** 5 SP

**Akzeptanzkriterien:**
- Die App nutzt optional den letzten bekannten Gerätestandort zur Schlafenszeit als Abfahrtspunkt.
- Weicht dieser mehr als 1 km von der hinterlegten Heimadresse ab, wird die Route neu berechnet.
- Die Nutzer:in wird informiert: „Route wird von aktuellem Standort berechnet."
- Die Funktion erfordert Standortfreigabe und ist opt-in.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-07 · Morgen-Briefing

**Als** Nutzerin
**möchte ich** beim Aufwachen ein personalisiertes Morgen-Briefing erhalten,
**damit** ich sofort die wichtigsten Informationen für den Tag kenne, ohne mehrere Apps öffnen zu müssen.

*Abgeleitet aus: Michael – Szenario 1 (Wetter, Verkehr, Parkplatz, Tor-Empfehlung); Anna – Szenario 1 & 3; Lukas – Szenario 2*

**Aufwandsschätzung:** 5 SP

**Akzeptanzkriterien:**
- Beim Auslösen des Alarms zeigt die App ein Briefing mit: erstem Termin des Tages (Zeit & Ort), aktuellem Wetter inkl. relevanter Warnungen (z. B. Glatteis), empfohlener Abfahrtszeit und geschätzter Fahrtdauer.
- Das Briefing erscheint automatisch ohne zusätzliche Interaktion.
- Die Nutzer:in kann konfigurieren, welche Module angezeigt werden (Wetter, Verkehr, Kalender).
- Bei fehlender Internetverbindung werden gecachte Daten als Fallback verwendet.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-08 · Einschlafempfehlung am Vorabend

**Als** Nutzer
**möchte ich** abends eine Push-Benachrichtigung erhalten, die mir empfiehlt, wann ich schlafen gehen sollte,
**damit** ich vor meinem nächsten Morgentermin ausreichend Schlaf bekomme.

*Abgeleitet aus: Michael – Szenario 1 („Wenn du um 21:00 schläfst, bekommst du 7 h 35 min"); Lukas – Szenario 1 & 3; Anna – Szenario 1*

**Aufwandsschätzung:** 3 SP

**Akzeptanzkriterien:**
- Basierend auf der berechneten Weckzeit und einer konfigurierbaren Ziel-Schlafdauer (Standard: 7,5 Stunden) berechnet die App eine empfohlene Einschlafzeit.
- Die Benachrichtigung wird zur empfohlenen Einschlafzeit gesendet (z. B. „Wenn du jetzt schläfst, bekommst du 7 h 35 min").
- Die Nutzer:in kann Ziel-Schlafdauer und Benachrichtigungszeitpunkt anpassen.
- Die Benachrichtigung kann für einzelne Nächte gesnoozed oder deaktiviert werden.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-09 · Später-Abend-Hinweis bei aktiver Nutzung

**Als** Nutzer
**möchte ich** einen sanften Hinweis erhalten, wenn ich spät abends noch aktiv bin und am nächsten Tag früh aufstehen muss,
**damit** ich rechtzeitig daran erinnert werde, schlafen zu gehen.

*Abgeleitet aus: Lukas – Szenario 1 („Um 1:00 Uhr, während Lukas noch unterwegs ist, sendet Pünktlich eine Smart Notification"); Lukas – Szenario 3*

**Aufwandsschätzung:** 3 SP

**Akzeptanzkriterien:**
- Wird das Gerät nach der empfohlenen Einschlafzeit noch aktiv genutzt und steht ein früher Alarm an, wird genau einmal eine Push-Benachrichtigung gesendet (z. B. „Hey Lukas, du hast morgen eine Vorlesung. Wenn du jetzt gehst, bekommst du 7 Stunden Schlaf.").
- Die Benachrichtigung nennt den konkreten bevorstehenden Termin.
- Sie wird pro Nacht und Termin nur einmal gesendet.
- Die Funktion kann in den Einstellungen deaktiviert werden.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-10 · Schlafzyklus-optimierter Alarm

**Als** Nutzerin
**möchte ich**, dass mein Alarm am Ende eines 90-Minuten-Schlafzyklus gesetzt wird,
**damit** ich trotz kurzer Schlafdauer ausgeruhter aufwache.

*Abgeleitet aus: Anna – Szenario 3 („optimaler Schlafzyklus", Wecker auf 7:15 Uhr); Michael – Szenario 1 & 2*

**Aufwandsschätzung:** 5 SP

**Akzeptanzkriterien:**
- Die App berechnet ausgehend von der benötigten Weckzeit den nächstgelegenen schlafzyklus-konformen Aufwachzeitpunkt (Fenster: ±30 Min, ohne dass die Nutzer:in zu spät kommt).
- Die Nutzer:in kann die Schlafzyklusoptimierung global oder pro Alarm aktivieren/deaktivieren.
- Die App zeigt an, wie viele vollständige Schlafzyklen die geplante Schlafdauer umfasst.
- Der optimierte Zeitpunkt liegt nie später als die ursprünglich erforderliche Weckzeit.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-11 · Schichtarbeiter-Schlafplan

**Als** Schichtarbeiter
**möchte ich** einen an meinen Schichttyp (Früh-, Spät- oder Nachtschicht) angepassten Schlaf- und Nickerchen-Plan erhalten,
**damit** ich trotz wechselnder Schichten ausreichend Schlaf bekomme.

*Abgeleitet aus: Michael – Szenario 2 (Power-Nap 12:30, Koffeinlimit) & Szenario 3 (prophylaktischer 90-Min-Vorschlaf, Licht-Tipps)*

**Aufwandsschätzung:** 5 SP

**Akzeptanzkriterien:**
- Die Nutzer:in kann einen Termin oder eine Schicht als „Frühschicht", „Spätschicht" oder „Nachtschicht" kennzeichnen.
- Die App erstellt daraufhin einen maßgeschneiderten Schlafplan: empfohlene Nickerchenfenster, Einschlafzeit und Hinweise zur Lichtsteuerung.
- Für Nachtschichten wird ein prophylaktisches Vorschlaffenster (z. B. 90 Min) vorgeschlagen.
- Der Plan wird am Nachmittag/Abend vor Schichtbeginn angezeigt.
- Einzelne Empfehlungen können abgelehnt oder angepasst werden.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-12 · Müdigkeitscheck vor der Heimfahrt

**Als** Schichtarbeiter
**möchte ich** nach einer Nachtschicht einen kurzen Reaktionstest absolvieren können,
**damit** ich eine Sicherheitsempfehlung erhalte, wenn ich zu müde zum Fahren bin.

*Abgeleitet aus: Michael – Szenario 3 („Müdigkeits-Check" mit Reaktionstest, 15-Min-Power-Nap auf dem Werksparkplatz bei Risikowerten)*

**Aufwandsschätzung:** 5 SP

**Akzeptanzkriterien:**
- Nach dem Ende eines Nachtschicht-Termins (oder auf Nutzeranfrage) bietet die App optional einen kurzen Reaktionstest an (≤ 60 Sekunden).
- Liegt das Ergebnis unterhalb eines konfigurierbaren Schwellenwerts, empfiehlt die App einen 15-minütigen Power-Nap und zeigt einen geeigneten Rastplatz in der Nähe an.
- Bei unauffälligem Ergebnis wird die Heimroute normal angezeigt.
- Der Test ist vollständig opt-in und kann jederzeit übersprungen werden.
- Testergebnisse werden nicht extern übermittelt.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-13 · Travel Mode für Reiseabfahrten

**Als** Nutzer
**möchte ich** für Zug- oder Flugreisen einen „Travel Mode" aktivieren können,
**damit** die App strengere Puffer anwendet, Snooze deaktiviert und mich an wichtige Reiseutensilien erinnert.

*Abgeleitet aus: Lukas – Szenario 3 (Snooze-Deaktivierung, Travel Mode); Anna – Szenario 1 (Flugticket, Gate-Infos)*

**Aufwandsschätzung:** 5 SP

**Akzeptanzkriterien:**
- Travel Mode kann manuell pro Termin aktiviert werden oder wird automatisch vorgeschlagen, wenn ein Flug- oder Zugtermin erkannt wird.
- Im Travel Mode: Snooze ist beim ersten Alarm deaktiviert, Ankunftspuffer beträgt mindestens 20 Minuten, und am Vorabend wird eine Reise-Checklisten-Benachrichtigung gesendet.
- Ein „Travel Mode aktiv"-Hinweis wird auf dem Alarm- und Briefing-Bildschirm angezeigt.
- Die Nutzer:in kann den Travel Mode pro Termin manuell aktivieren oder deaktivieren.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-14 · Abend-Checklisten-Erinnerung

**Als** Nutzer
**möchte ich** am Vorabend eines wichtigen Termins eine Erinnerung mit einer Checkliste der vorzubereitenden Dinge erhalten,
**damit** ich nichts Wichtiges vergesse (z. B. Ausweis, Schutzausrüstung, Bewerbungsunterlagen).

*Abgeleitet aus: Michael – Szenario 1 („Leg Arbeitsjacke, Ausweis und Gehörschutz bereit"); Lukas – Szenario 2 (Outfit bereitlegen)*

**Aufwandsschätzung:** 3 SP

**Akzeptanzkriterien:**
- Die App sendet am Vorabend eines Termins eine Erinnerungsbenachrichtigung (Uhrzeit konfigurierbar, Standard: 21:00 Uhr).
- Die Erinnerung enthält eine anpassbare Checkliste. Standardeinträge je Termintyp: Schicht (PSA, Ausweis), Vorstellungsgespräch (Outfit, Unterlagen), Reise (Ticket, Reisepass, Ladekabel).
- Die Nutzer:in kann Einträge hinzufügen, entfernen und neu anordnen – pro Termin oder global.
- Einträge können direkt aus der Benachrichtigung als „vorbereitet" markiert werden.

**Definition of Done:** Siehe gemeinsamen DoD.

---

### US-15 · Nutzerprofil & Personalisierung

**Als** neue Nutzer:in
**möchte ich** mein Profil mit Heimadresse, bevorzugtem Verkehrsmittel, Vorbereitungszeit und Schlafzieldauer einrichten,
**damit** *Pünktlich.* von Beginn an genaue Berechnungen liefert.

*Abgeleitet aus: Allen Personas – Grundlage für alle personalisierten Berechnungen*

**Aufwandsschätzung:** 3 SP

**Akzeptanzkriterien:**
- Ein Onboarding-Flow erfasst: Heimadresse, Standard-Verkehrsmittel (Auto / ÖPNV / zu Fuß), durchschnittliche Morgen-Vorbereitungszeit (Minuten) und Ziel-Schlafdauer pro Nacht.
- Alle Felder sind optional; bei übersprungenen Feldern werden sinnvolle Standardwerte verwendet.
- Profildaten können jederzeit in den Einstellungen aktualisiert werden.
- Die App verwendet Profildaten als Basis für alle Berechnungen; Überschreibungen pro Termin bleiben möglich.

**Definition of Done:** Siehe gemeinsamen DoD.
