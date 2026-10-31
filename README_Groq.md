# Hermes AI Agent – Installation und erster Teamtest

**Schritt 1: Einrichtung bis zum 03.11.2026**

Wir untersuchen, welche Aufgaben Hermes mit einem Sprachmodell und Werkzeugen selbstständig bearbeiten kann. Für den Einstieg verwenden wir Groq als Modellanbieter und `openai/gpt-oss-120b` als Modell.

Diese Anleitung beschreibt die Einrichtung von Hermes Agent in Docker.

## 1. Docker installieren

### 1.1 Docker unter Windows installieren

#### 1.1.1 Voraussetzungen prüfen

Für diese Anleitung verwenden wir Docker Desktop mit WSL 2 und Linux-Containern.

1. Die aktuelle [Windows-Installationsseite von Docker](https://docs.docker.com/desktop/setup/install/windows-install/) öffnen und prüfen, ob die eigene Windows-Version unterstützt wird.

2. Im Task-Manager unter **Leistung → CPU** nach **Virtualisierung: Aktiviert** schauen. Bei deaktivierter Virtualisierung muss sie gegebenenfalls im BIOS/UEFI eingeschaltet werden.

3. Für den WSL-2-Weg nennt Docker derzeit unter anderem 8 GB Arbeitsspeicher und WSL ab Version 2.1.5. Die verlinkte Seite enthält die vollständigen Anforderungen.

#### 1.1.2 Docker Desktop installieren

1. [Docker Desktop für Windows](https://docs.docker.com/desktop/setup/install/windows-install/) öffnen.

### 1.2 Docker unter macOS installieren

1. Die [Docker-Installationsseite für macOS](https://docs.docker.com/desktop/setup/install/mac-install/) öffnen.

2. Die heruntergeladene `.dmg` öffnen.

3. Docker in den Ordner **Programme / Applications** ziehen.

4. Docker aus **Programme** starten.

5. Die angezeigten Einrichtungsschritte abschließen und erforderliche Berechtigungen erteilen.

6. Warten, bis Docker Desktop die laufende Engine anzeigt.

7. Die App **Terminal** öffnen und mit Abschnitt 2 fortfahren.

## 2. Docker prüfen und Projektordner öffnen

### 2.1 Installation überprüfen

Dieser Befehl funktioniert in PowerShell sowie im macOS-/Linux-Terminal:

```text
docker --version
```

### 2.2 Repository lokal bereitstellen

Das Repository klonen:

```text
git clone https://github.com/TutaevaIrina/hermes-ai-agent.git
```

## 3. Groq-Zugang vorbereiten

1. Die [Groq Console](https://console.groq.com/) öffnen.

2. Ein eigenes Konto erstellen oder anmelden.

3. Unter [API Keys](https://console.groq.com/keys) einen API-Schlüssel anlegen.

4. Den Schlüssel für die anschließende lokale Eingabe bereithalten.

### Gemeinsame Konfiguration

Modell-ID: `openai/gpt-oss-120b`

**Limits des kostenlosen Zugangs, Stand 22.10.2026:** Die öffentliche Groq-Tabelle nennt für dieses Modell im Free Plan 30 Anfragen pro Minute, 1.000 pro Tag, 8.000 Tokens pro Minute und 200.000 Tokens pro Tag.

Eine Agentenaufgabe kann mehrere Modellanfragen auslösen. Auch Systemtext, Werkzeugbeschreibungen und bisherige Nachrichten benötigen Tokens. Ein großes Kontextfenster hebt das Tokenlimit pro Minute nicht auf. Daher starten wir mit kurzen Aufgaben und wenigen Werkzeugen.

Quellen: [Groq Quickstart](https://console.groq.com/docs/quickstart), [OpenAI-Kompatibilität](https://console.groq.com/docs/openai), [Modellbeschreibung](https://console.groq.com/docs/model/openai/gpt-oss-120b), [Rate Limits](https://console.groq.com/docs/rate-limits).

## 4. Hermes-Image herunterladen und Daten-Volume anlegen

Die folgenden Befehle gelten für alle drei Betriebssysteme:

```text
docker pull nousresearch/hermes-agent:stable
docker volume create hermes-test-data
```

Prüfen:

```text
docker image ls nousresearch/hermes-agent
docker volume inspect hermes-test-data
```

Quelle: [Hermes in Docker](https://hermes-agent.nousresearch.com/docs/user-guide/docker).

## 5. Groq und das Modell in Hermes einrichten

### 5.1 Modellauswahl öffnen

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable model
```

Wenn zunächst eine Anbieterliste erscheint, **Custom / OpenAI-compatible endpoint** oder die sinngleiche Option auswählen. Menünamen können je nach Version abweichen.

**API base URL:**

```text
https://api.groq.com/openai/v1
```

**API key:**

Den eigenen Groq-Schlüssel eingeben. Eine verdeckte oder aus Sternchen bestehende Anzeige ist normal.

**Select API compatibility mode:**

```text
2. Chat Completions
```

`2` ist die Nummer im bisher beobachteten Menü. Wenn sich die Reihenfolge ändert, die Option anhand des Textes `Chat Completions` auswählen.

**Select model:**

```text
openai/gpt-oss-120b
```

Den Modellnamen eingeben oder den passenden Listeneintrag auswählen. Im bisherigen Setup war es Eintrag `10`; diese Nummer kann bei anderen Konten oder späteren Versionen anders sein.

**Context length in tokens [leave blank for auto-detect]:**

Ohne Eingabe **Enter** drücken. Hermes darf die Kontextgröße automatisch ermitteln.

**Display name:**

```text
Groq
```

**Select reasoning effort:**

Mit den Pfeiltasten `low` wählen und mit **Enter** bestätigen. Das ist unsere Starteinstellung für einfache Tests. Ein geringerer Denkaufwand kann den Tokenverbrauch begrenzen, garantiert aber kein bestimmtes Kosten- oder Qualitätsniveau.

Wenn eine weitere Frage erscheint, anhand ihrer Beschreibung entscheiden. Für diesen Einstieg sind weder ein Messaging-Gateway noch Telegram oder Discord erforderlich. Eine angebotene zusätzliche kostenpflichtige Anbieteranbindung gehört nicht zu diesem Setup.

Nach dem Speichern endet der Konfigurationsprozess üblicherweise und das Host-Terminal erscheint wieder. Eine vorher angezeigte Standardmodell-ID allein bestätigt noch keine funktionierende Anbieteranbindung; entscheidend ist später die erfolgreiche erste Antwort.

### 5.2 Terminal-Backend festlegen

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable config set terminal.backend local
```

**Warum `local`?** Hermes läuft bereits in einem Docker-Container. Sein lokales Terminal arbeitet deshalb innerhalb dieses Containers. Ein zusätzliches Docker-Terminal-Backend wäre ein anderer Aufbau.

Anbieter- und Modelleinstellungen lassen sich später mit dem Befehl aus Abschnitt 5.1 erneut ändern. Ein eigener Eintrag `GROQ_MODEL=...` aus einem früheren Python-Projekt konfiguriert Hermes nicht automatisch.

Quellen: [Hermes-Modellanbieter](https://hermes-agent.nousresearch.com/docs/integrations/providers), [Hermes-Konfiguration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration).

## 6. Hermes starten und den ersten Test durchführen

### 6.1 Chat mit wenigen Werkzeugen starten

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable chat --toolsets "terminal,file"
```

Die Werkzeugauswahl begrenzt den ersten Versuch auf Terminal und Dateibearbeitung. Das reduziert zugleich den Umfang der Werkzeugbeschreibungen im Modellkontext.

Im Chat werden normale Aufgaben eingegeben. Docker-Befehle aus dieser Anleitung gehören dagegen in das Terminal des eigenen Rechners.

### 6.2 Verbindungstest

Zunächst eingeben:

> Antworte kurz auf Deutsch: Welches Modell wird in dieser Sitzung verwendet?

Für die tatsächlich konfigurierte Modell-ID zusätzlich die Startanzeige bzw. `/model` betrachten; eine Selbstauskunft des Modells ist kein verlässlicher Konfigurationsnachweis.

### 6.3 Werkzeug- und Dateitest

Anschließend diese Aufgabe eingeben:

> Lege das Verzeichnis /opt/data/team-tests an. Erstelle darin die Datei hermes-test.txt mit genau dem Inhalt „Hallo Team“. Lies die Datei anschließend mit einem Werkzeug wieder ein und zeige mir den gelesenen Inhalt sowie den vollständigen Dateipfad.

**Erwartet wird:**

- Eine echte Datei unter `/opt/data/team-tests/hermes-test.txt`.

- Eine sichtbare Werkzeugaktion, beispielsweise über Terminal oder Dateifunktionen.

- Eine Antwort mit dem Inhalt `Hallo Team`.

- Keine bloße Beschreibung, wie man die Datei selbst erstellen könnte.

Falls Hermes eine Bestätigung für die konkrete Aktion verlangt, die angezeigte Aktion lesen und passend zum Test beantworten.

### 6.4 Ergebnis unabhängig prüfen

Den Chat mit `/quit` beenden. Anschließend im Host-Terminal ausführen:

```text
docker run --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable bash -lc "cat /opt/data/team-tests/hermes-test.txt"
```

Es sollte `Hallo Team` ausgegeben werden. Diese Prüfung liest die Datei direkt und benötigt keine Modellanfrage.

Der neue Container kann die Datei sehen, weil sie im Volume liegt. Eine Datei unter `/tmp` wäre dafür kein geeigneter Persistenztest.

Optional dieselbe Prüfung nach einem weiteren Hermes-Start wiederholen. Falls der Start mit `bash` in einer abweichenden Image-Version anders behandelt wird, die unterstützten Aufrufmuster der offiziellen Docker-Anleitung prüfen.

### 6.5 Erfolgskriterien

| Prüfung | Erfolgskriterium |
| --- | --- |
| Docker | Client und Server sind erreichbar; `hello-world` funktioniert |
| API-Zugang | Hermes erhält eine Modellantwort |
| Modellkonfiguration | `openai/gpt-oss-120b` wird als gewähltes Modell angezeigt |
| Werkzeuge | Die Datei wird tatsächlich erstellt und eingelesen |
| Persistenz | Ein neu gestarteter Container kann dieselbe Datei lesen |

Quelle für Werkzeugauswahl und CLI: [Tools & Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools), [CLI Interface](https://hermes-agent.nousresearch.com/docs/user-guide/cli).
