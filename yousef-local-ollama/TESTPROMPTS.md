# Prompts zum Kopieren

Die Ergebnisreferenz steht in `VERSUCHE.md`. Dies ist eine Sammlung bereits verwendeter bzw. unmittelbar daraus abgeleiteter Kontrollprompts; durch das Anlegen dieser Datei wurde kein neuer Versuch ausgeführt.

## Vorbereitung je Gespräch

Im Hermes-Chat jeweils einzeln eingeben und den bestätigten Zustand protokollieren:

```text
/new
```

```text
/reasoning none
```

Bei einem gesonderten Vergleichslauf stattdessen nach `/new` die Stufe `/reasoning medium` setzen. Modell, Tools, Skills, Datenbestand und Durchlaufgrenze zusätzlich festhalten.

## Verbindung prüfen

```text
Antworte ausschließlich mit: Verbindung funktioniert.
```

Dieser kurze Prompt prüft, ob eine Chat-Antwort ankommt. Er prüft keine Werkzeug- oder Recherchequalität.

## Datei erstellen und lesen

```text
Lege das Verzeichnis /opt/data/team-tests an. Erstelle darin die Datei hermes-test.txt mit genau dem Inhalt „Hallo Team“. Lies die Datei anschließend mit einem Werkzeug wieder ein und zeige den gelesenen Inhalt.
```

Unabhängige Kontrolle bei laufendem Dashboard in PowerShell:

```powershell
docker exec hermes-web cat /opt/data/team-tests/hermes-test.txt
```

## Öffentliche Daten selbstständig finden

```text
Wie viele Personen waren am 31.12.2024 im Berliner Einwohnerregister mit Hauptwohnung gemeldet? Suche selbstständig eine geeignete öffentliche Quelle und belege deine Antwort.
```

## Gezielter Ausschnitt aus der vorbereiteten Datei

Voraussetzung: Die beschriebene Markdown-Datei liegt mit genau diesem Zeilenstand vor. Die Zeilennummer ist keine stabile Kennung anderer Konvertierungen.

```text
Lies mit read_file die Datei /opt/data/team-tests/berlin_2024.md, beschränkt auf die Zeilen 1380 bis 1430.

Wie viele Personen waren am 31.12.2024 im Berliner Einwohnerregister mit Hauptwohnung gemeldet? Verwende den Gesamtwert „Insgesamt“ aus der Zeile „Berlin“.

Nenne die Einwohnerzahl und zitiere die gelesene Tabellenzeile als Beleg.
```

## Einzelne Zeile als Kontrolle

```text
Lies mit read_file aus /opt/data/team-tests/berlin_2024.md genau die Zeile 1427. Gib die Zeile vollständig und wörtlich aus. Nenne anschließend die erste Zahl nach dem Zelltext „Berlin“. Nutze ausschließlich diese Zeile.
```

## Protokoll je neuem Versuch

| Feld | Eintrag |
| --- | --- |
| Datum und testende Person | |
| Hermes-Version und Image-Digest | |
| Modell, Modell-Digest, Kontext | |
| Reasoning und Durchlaufgrenze | |
| Tools und Skills | |
| Daten-/Sitzungsvorbereitung | |
| Exakter Prompt | |
| Werkzeugaktionen und Fehler | |
| Tatsächliche Antwort | |
| Manuelle Hilfen | |
| Angezeigte Dauer | |
| Unabhängiger Beleg und Bewertung | |

Vor Veröffentlichung eines Protokolls persönliche Inhalte und Zugangsdaten aus vollständigen Rohlogs entfernen.
