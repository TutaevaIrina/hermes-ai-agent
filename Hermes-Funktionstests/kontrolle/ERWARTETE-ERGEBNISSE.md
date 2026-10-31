# Erwartete Ergebnisse für das Team

Diese Datei enthält die Prüfergebnisse für die fiktiven Eingabedateien. Nicht als Informationsquelle für Hermes verwenden. Stand: 30.10.2026.

## 1 CSV lesen

13 Datenzeilen ohne Kopfzeile; 7 Spalten: `schul_id`, `schulname`, `bezirk_id`, `schulart`, `traegerschaft`, `anschrift`, `schuelerzahl`. Trennzeichen Semikolon; UTF-8 mit BOM. Die 13 Zeilen beschreiben 12 unterschiedliche Schul-IDs.

## 2 CSV filtern

Genau 2 Schulen: T001, Testschule Birke, Teststraße 1, 13051 Berlin; T002, Testschule Kastanie, Teststraße 2, 13051 Berlin. Die Ausgabe enthält Kopfzeile und zwei Datenzeilen mit allen sieben Originalspalten. T002 wird trotz doppelter Eingabe nur einmal ausgegeben.

## 3 Datenqualität

Die CSV-Zeilen 3 und 14 sind vollständig identisch (T002). Eine zusätzliche Dublette ist zu entfernen, wenn unterschiedliche Schulen gezählt werden. Leere Anschrift: T004, CSV-Zeile 5. Fehlende Schülerzahl: T009, CSV-Zeile 10. Sonst keine leeren Felder. Zeilennummern hier einschließlich Kopfzeile; unbekannte Schülerzahl nicht erfinden oder als belegte Null ausgeben.

## 4 PDF lesen

Titel: Berliner Schulwege im Funktionstest. Verfasser: Projektteam Beispiel. Stand: 30.10.2026. Genau 2 PDF-Seiten. Alle Projektangaben sind erfunden; kein tatsächlicher Projektbericht.

## 5 PDF Informationen

Projektstart 02.11.2026, Abgabetermin 16.11.2026, fiktives Budget 120 Euro. Alle drei Angaben stehen auf PDF-Seite 1. Auf Seite 2 stehen: Dateien lesen, Daten prüfen und Ergebnisse sichern. Sinngemäße Zusammenfassung zulässig.

## 6 Word lesen

Besprechung 30.10.2026; Anna Beispiel, Ben Muster, Cem Test. Die exportierte CSV enthält drei Aufgaben:

| aufgabe | verantwortlich | termin |
| --- | --- | --- |
| CSV-Prüfung | Anna Beispiel | 04.11.2026 |
| PDF-Prüfung | Ben Muster | 06.11.2026 |
| Gesamtbericht | Cem Test | 16.11.2026 |

## 7 Word Kopie ändern

In der Quelldatei steht 16.11.2026 genau zweimal: im dritten Beschluss und in der Tabellenzeile Gesamtbericht. In der Kopie steht jeweils 18.11.2026; kein 16.11.2026 bleibt zurück. Die Quelle ist byteweise unverändert. Titel, Teilnehmende, andere Termine und Tabelle bleiben erhalten.

## 8 Markdown lesen

Leere Schülerzahl bedeutet unbekannt. Beide CSV-Dateien werden über bezirk_id verbunden; führende Nullen bleiben erhalten. Vollständig identische Zeilen zählen bei der Zahl unterschiedlicher Schulen nur einmal.

## 9 Markdown erstellen

Nur notiz-fertig.md vorhanden; notiz-entwurf.md fehlt. Inhalt genau drei Zeilen; ein abschließender Zeilenumbruch ist zulässig:

```markdown
# Dateitest
Status: erfolgreich
Daten: fiktiv
```

## 10 CSV Dateien verbinden

| bezirk_id | bezirk | anzahl_schulen | summe_bekannte_schuelerzahlen | fehlende_schuelerzahlen |
| --- | --- | --- | --- | --- |
| 01 | Mitte | 2 | 1100 | 0 |
| 02 | Friedrichshain-Kreuzberg | 2 | 380 | 1 |
| 03 | Pankow | 3 | 1830 | 0 |
| 11 | Lichtenberg | 5 | 1930 | 0 |

Insgesamt 12 unterschiedliche Schulen. Die Summen sind ausschließlich Summen bekannter Werte; für Friedrichshain-Kreuzberg ist die gesamte Schülerzahl damit nicht bestimmt. Alle 12 IDs finden genau einen Bezirksnamen. Ausgabe aufsteigend nach Bezirkskennung.

## 11 PDF kopieren

Original und Kopie existieren, haben jeweils 2 Seiten und denselben SHA-256-Prüfwert. Die reine Umbenennung einer unveränderten Kopie verändert die Bytes nicht.

## 12 Word Bericht

Eine neu erzeugte, lesbare Word-Datei mit genau einer gerenderten Seite. Enthalten: Hinweis auf fiktive Daten; Start 02.11.2026, Abgabe 16.11.2026, Budget 120 Euro; Bezirkstabelle mit Mitte 2, Friedrichshain-Kreuzberg 2, Pankow 3 und Lichtenberg 5 unterschiedlichen Schulen; eine zusätzliche identische Zeile T002; fehlende Anschrift T004 und fehlende Schülerzahl T009. Die geänderte Kopie aus Aufgabe 7 ist keine Quelle. Erneutes Einlesen muss die Inhalte bestätigen.

## Bewertung

Je Aufgabe getrennt notieren: fachliche Richtigkeit, sichtbare Werkzeugnutzung, vorhandene Ausgabedatei, unabhängige Prüfung und benötigte Hilfestellung. Ein API-Abbruch oder eine fehlende Bibliothek ist ein technischer Fehler und kein Beleg für ein fachlich falsches Rechenergebnis.
