# Bisherige Versuche und technische Kontrollen

Zusammenfassung der in dieser Zusammenarbeit bereitgestellten Ausgaben; Dokumentationsstand 25.10.2026. Die Uhrzeiten einzelner Versuche werden hier nicht zu zusätzlichen Datumsangaben ergänzt. Die IDs in dieser Tabelle ordnen die beschriebenen Chat-Versuche und ersetzen keine vorhandenen Runner-IDs wie B02.

| Versuch | Unterstützung / Aufgabe | Beobachtung | Bewertung | Angezeigte Dauer |
| --- | --- | --- | --- | --- |
| T01 | Datei `hermes-test.txt` mit „Hallo Team“ erstellen und lesen | Schreiben und Lesen gelangen; unabhängiges `cat` in neuem Container bestätigte den Inhalt | Dateifunktion und Volume-Persistenz bestätigt | 2:58 |
| T02 | Berlin-Frage vor Web-Konfiguration | Lokale Suche und ungeeignete URL-Versuche; kein abschließendes Ergebnis überliefert | Unvollständiger Vorversuch | kein Endwert |
| T03 | Berlin-Frage mit selbstständiger Quellensuche | Falsche Zahl 768.915; kein nachgewiesenes Ablesen der Gesamtzahl | Nicht gelöst | 3:08 |
| T04 | Quelle suchen, abrufen und nur belegte Zahl nennen | DDGS-Fetch scheiterte als Search-only-Backend; curl ohne Dateiausgabe; 8 Iterationen erreicht; keine Zahl | Nicht gelöst, Zahl wurde zurückgehalten | 3:12 |
| T05 | Exakte PDF-URL, Speicherpfad und Seite vorgegeben | PDF abgerufen; Hermes behauptete, keine Gesamtzeile finden zu können | Nicht gelöst | 4:03 |
| T06 | Vorbereitete Markdown-Datei, Zeilen 1380–1430, Reasoning aus | Falsche Auswahl 274.098 aus der vorangehenden Bezirks-Zusammen-Zeile | Nicht gelöst | 2:06 |
| T07 | Exakt Zeile 1427 und erste Zahl nach Berlin verlangt | Richtige Berlin-Zeile mit 3 897 145 enthalten; zusätzlicher Präfix, Zahl nicht separat genannt; Werkzeug las drei Zeilen | Teilweise erfüllt | 1:26 |
| T08 | Wie T06, neue Sitzung und Reasoning medium bestätigt | Finale Antwort 2.925.267, eine Teilpopulation der Berlin-Zeile | Nicht gelöst | 4:45 |

Die Dauern stammen aus den jeweiligen UI-Zusammenfassungen. Sie messen nicht den gesamten Einrichtungs- und Unterstützungsaufwand.

## Manuelle Datenkontrolle

Im verwendeten Container fehlte `pdftotext`. Auch `pypdf`, `PyPDF2`, `pymupdf`, `fitz` und `pdfplumber` waren im damaligen Modultest nicht vorhanden. `anydoc` war vorhanden.

Die PDF wurde unabhängig von Hermes mit `anydoc.to_markdown()` umgewandelt: 236.829 extrahierte Zeichen, 38 gefilterte Berlin-Treffer. Diese manuelle Vorbereitung zählt als Unterstützung, nicht als autonome Hermes-Leistung.

Zeile 1427 der genau dabei erzeugten Markdown-Datei:

```text
||Berlin|3 897 145|100|1 601 865|41,1|2 925 267|75,1|2 295 280|58,9|629 987|16,2|971 878|24,9|
```

Die amtliche Gesamtzahl mit Hauptwohnung am 31.12.2024 beträgt **3.897.145**. Die Zahl **2.925.267** steht für deutsche Einwohnerinnen und Einwohner; **971.878** für ausländische. Die vorangehende Bezirks-Zusammen-Zeile mit **274.098** gehört zu Reinickendorf.

Quelle: Amt für Statistik Berlin-Brandenburg, *Einwohnerregisterstatistik Berlin 31. Dezember 2024*, A I 16 – hj 2/24, gedruckte Seite **27**.

- [Direkte PDF](https://download.statistik-berlin-brandenburg.de/9673209d56d43e64/bd35b2b2f78d/SB_A01-16-00_2024h02_BE.pdf)
- [Amtliche Pressemitteilung Nr. 25/2025](https://www.statistik-berlin-brandenburg.de/025-2025/)

## Oberfläche und Verbindung

- Der Dashboard-Befehl war im verwendeten Image verfügbar.
- Der lokale Dashboard-Start gelang nach Behebung eines Profilkonflikts durch zwei Container am selben Volume.
- Der Chat-Verbindungstest wurde korrekt beantwortet.
- Im Modellmenü stand `custom · hermes-projekt:latest`.
- Die tatsächlich ausgelesene Base URL lautete `http://host.docker.internal:11434/v1`.
- Das Formular für `agent.max_turns` zeigte anschließend 8; Speichern und aktive Übernahme sind vor einer neuen Messreihe zu prüfen.
- Der gemeinsame Zugriff über Tailscale wurde noch nicht bestätigt.

## Aussagegrenzen und nächste Arbeit

Es wurde bisher eine inhaltliche Open-Data-Frage mit unterschiedlichen Hilfen untersucht. Für den vergleichbaren Zeilenausschnitt liegt je ein gezeigter Lauf ohne Reasoning und mit medium vor. Beide Antworten waren falsch; aus je einem Lauf folgt keine allgemeine Aussage über Reasoning oder das Modell.

Neue Wiederholungen, CSV-Auswertungen und Mehrdatensatzfragen sind als weitere Arbeit vorgesehen. Sie werden in diesem Dokument nicht als durchgeführt ausgewiesen. Vor Wiederholungen sind Toolsets und Skills anzugleichen oder als eigene Bedingung zu dokumentieren.

Ein neues Gespräch setzt nicht automatisch heruntergeladene Dateien, dauerhafte Erinnerungen oder Skills zurück. Für belastbare Vergleichsreihen ist die Daten- und Sitzungsvorbereitung ausdrücklich festzuhalten.
