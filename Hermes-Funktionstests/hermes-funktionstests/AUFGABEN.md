# Aufgaben für Hermes zum Testen von Dateifunktionen

Die Aufgaben prüfen Werkzeuge mit bewusst kleinen, fiktiven Eingabedateien. Sie sind von den inhaltlichen Open-Data-Hauptfragen getrennt. Jede Aufgabe wird einzeln in einer neuen Sitzung mit denselben Originaldateien durchgeführt. Internetrecherche ist nicht erforderlich.

## Gemeinsame Anweisung

Führe die Aufgabe tatsächlich mit Werkzeugen aus. Erstelle bei Bedarf den Unterordner `ergebnisse`. Prüfe erzeugte Dateien durch erneutes Lesen. Nenne vollständige Ausgabepfade. Dokumentiere fehlende Dateien, fehlende Programme oder andere konkrete Fehler. Erfinde keine Inhalte oder erfolgreichen Aktionen. Verändere keine Eingabedatei. Falls eine Ausgabedatei vom vorherigen Versuch existiert, brich ab und melde dies, damit das Team den Testordner zurücksetzen kann.

## 1. CSV lesen (Leicht)

Lies die CSV-Datei unter `/workspace/hermes-funktionstests/schulen.csv`. Nenne die Spaltennamen und die Anzahl der Datenzeilen ohne Kopfzeile. Nenne außerdem Trennzeichen und Zeichencodierung.

## 2. CSV filtern (Mittel)

Lies `/workspace/hermes-funktionstests/schulen.csv`. Ermittle die öffentlichen Grundschulen mit `bezirk_id` 11. Zähle jede `schul_id` nur einmal. Nenne Schulname und Anschrift und speichere die gefilterten Zeilen mit allen Originalspalten als `/workspace/hermes-funktionstests/ergebnisse/grundschulen-lichtenberg.csv`.

## 3. Datenqualität prüfen (Mittel)

Prüfe `/workspace/hermes-funktionstests/schulen.csv` auf vollständig identische Zeilen und leere Felder. Nenne betroffene `schul_id`, Spalten und CSV-Zeilennummern einschließlich Kopfzeile. Verändere die Quelldatei nicht.

## 4. PDF lesen (Leicht)

Lies `/workspace/hermes-funktionstests/projektbericht.pdf`. Nenne Titel, Verfasser, Datenstand und die Anzahl der PDF-Seiten. Erkläre, ob es sich um einen echten Projektbericht oder eine Beispieldatei handelt.

## 5. PDF Informationen entnehmen (Mittel)

Lies `/workspace/hermes-funktionstests/projektbericht.pdf`. Nenne Projektstart, Abgabetermin und Budget jeweils mit PDF-Seitenzahl. Fasse die drei Arbeitsschritte auf Seite 2 in höchstens drei Sätzen zusammen.

## 6. Word lesen (Leicht)

Lies `/workspace/hermes-funktionstests/besprechungsprotokoll.docx`. Nenne Besprechungsdatum, Teilnehmende und die drei Aufgaben mit verantwortlicher Person und Termin. Speichere die Aufgaben als `/workspace/hermes-funktionstests/ergebnisse/aufgaben.csv` mit den Spalten `aufgabe`, `verantwortlich`, `termin`.

## 7. Word Kopie ändern (Mittel)

Erstelle eine Kopie von `/workspace/hermes-funktionstests/besprechungsprotokoll.docx` unter `/workspace/hermes-funktionstests/ergebnisse/protokoll-aktualisiert.docx`. Ersetze darin alle Vorkommen des Abgabetermins `16.11.2026` durch `18.11.2026`, auch in Tabellen. Erhalte die übrigen Inhalte und die Struktur. Prüfe durch erneutes Einlesen, ob die Änderung vollständig ist und die Quelldatei unverändert blieb.

## 8. Markdown lesen (Leicht)

Lies `/workspace/hermes-funktionstests/datenbeschreibung.md`. Nenne die Bedeutung leerer Schülerzahl-Felder, den Schlüssel zur Verknüpfung der beiden CSV-Dateien und die Regel zum Umgang mit vollständig identischen Zeilen.

## 9. Markdown erstellen und umbenennen (Leicht)

Erstelle `/workspace/hermes-funktionstests/ergebnisse/notiz-entwurf.md` mit genau drei Zeilen: Zeile 1 `# Dateitest`, Zeile 2 `Status: erfolgreich`, Zeile 3 `Daten: fiktiv`. Benenne die Datei anschließend in `notiz-fertig.md` um. Prüfe Inhalt, neuen Pfad und das Fehlen des alten Dateinamens.

## 10. Zwei CSV Dateien verbinden (Schwer)

Lies `/workspace/hermes-funktionstests/schulen.csv` und `/workspace/hermes-funktionstests/bezirke.csv`. Verknüpfe sie über `bezirk_id` und zähle jede `schul_id` nur einmal. Ermittle je Bezirk die Anzahl der Schulen, die Summe bekannter Schülerzahlen und die Anzahl fehlender Schülerzahlen. Speichere `/workspace/hermes-funktionstests/ergebnisse/bezirksuebersicht.csv` mit `bezirk_id`, `bezirk`, `anzahl_schulen`, `summe_bekannte_schuelerzahlen`, `fehlende_schuelerzahlen`, sortiert nach Bezirkskennung. Werte unbekannte Schülerzahlen nicht als belegte Null.

## 11. PDF kopieren und benennen (Mittel)

Kopiere `/workspace/hermes-funktionstests/projektbericht.pdf` nach `/workspace/hermes-funktionstests/ergebnisse/schulwege-kopie.pdf`. Prüfe, ob beide Dateien existieren, dieselbe PDF-Seitenzahl haben und byteweise identisch sind.

## 12. Ergebnisse als Word Bericht erstellen (Schwer)

Lies beide CSV-Dateien, `/workspace/hermes-funktionstests/datenbeschreibung.md` und `/workspace/hermes-funktionstests/projektbericht.pdf`. Erstelle einen einseitigen Word-Bericht unter `/workspace/hermes-funktionstests/ergebnisse/kurzbericht.docx`. Er soll den Hinweis auf fiktive Daten, Projektstart, Abgabetermin und Budget sowie eine Tabelle mit der Anzahl unterschiedlicher Schulen je Bezirk enthalten. Erwähne außerdem doppelte Zeilen und fehlende Angaben. Öffne die erzeugte Datei erneut und prüfe die gespeicherten Inhalte. Verwende nur die ursprünglichen Eingabedateien, keine Ergebnisse früherer Aufgaben.
