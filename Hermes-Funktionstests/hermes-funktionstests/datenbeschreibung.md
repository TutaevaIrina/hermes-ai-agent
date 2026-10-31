# Datenbeschreibung für den Hermes Funktionstest

**Alle Schulen, Anschriften, Personen und Projektangaben in diesem Paket sind frei erfunden.** Die Bezirksnamen sind reale Berliner Bezeichnungen; die Tabellen sind keine amtlichen Open Data. Stand: 30.10.2026.

## Dateien

| Datei | Inhalt |
| --- | --- |
| schulen.csv | Fiktive Schulen mit Merkmalen und Schülerzahlen |
| bezirke.csv | Zuordnung der Bezirkskennungen zu Bezirksnamen |
| projektbericht.pdf | Fiktiver Projektplan auf zwei textbasierten PDF-Seiten |
| besprechungsprotokoll.docx | Fiktive Besprechung mit Beschlüssen und Aufgaben |

## CSV Format

- Zeichencodierung: UTF-8 mit BOM.
- Trennzeichen: Semikolon.
- Erste Zeile: Spaltennamen; sie zählt nicht als Datenzeile.
- Leere Felder bedeuten unbekannt, nicht null Schüler.
- `schul_id` identifiziert eine Schule; `bezirk_id` wird als Text mit führender Null gelesen.
- Zusammenführung: `schulen.bezirk_id` mit `bezirke.bezirk_id`.
- `schuelerzahl` ist eine ganze Zahl oder leer. Summen beziehen sich nur auf vorhandene Angaben; fehlende Werte zusätzlich ausweisen.
- `traegerschaft` hat die Werte `öffentlich` und `privat`.

## Regeln für die Auswertung

Eine vollständig identische Zeile darf für die Zahl unterschiedlicher Schulen nur einmal gezählt werden. Fehlende Angaben nicht erfinden. Die Quelldateien bleiben unverändert. Alle neu erzeugten Dateien gehören in den Unterordner `ergebnisse`.
