# Hermes AI Agent – Installation und erster Teamtest mit HTW KIWI

**Schritt 1: Einrichtung bis zum 03.11.2026**

Wir untersuchen, welche Aufgaben Hermes mit einem Sprachmodell und Werkzeugen selbstständig bearbeiten kann. Für den Einstieg verwenden wir den über das KIW-Projekt der HTW Berlin bereitgestellten KIWI-API-Zugang und `qwen3.8-27b` als Modell.

Diese Anleitung beschreibt die Einrichtung von Hermes Agent in Docker. Das Sprachmodell läuft auf einem HTW-Server und wird über die API angesprochen.

## 1. Docker installieren

### 1.1 Docker unter Windows installieren

#### 1.1.1 Voraussetzungen prüfen

Für diese Anleitung verwenden wir Docker Desktop mit WSL 2 und Linux-Containern.

1. Die aktuelle [Windows-Installationsseite von Docker](https://docs.docker.com/desktop/setup/install/windows-install/) öffnen und prüfen, ob die eigene Windows-Version unterstützt wird.
2. Im Task-Manager unter **Leistung → CPU** nach **Virtualisierung: Aktiviert** schauen. Bei deaktivierter Virtualisierung muss sie gegebenenfalls im BIOS/UEFI eingeschaltet werden.
3. Für den WSL-2-Weg nennt Docker derzeit unter anderem 8 GB Arbeitsspeicher und WSL ab Version 2.1.5. Die verlinkte Seite enthält die vollständigen Anforderungen.

#### 1.1.2 Docker Desktop installieren

1. [Docker Desktop für Windows](https://docs.docker.com/desktop/setup/install/windows-install/) öffnen und der dortigen Installationsanleitung folgen.
2. Docker Desktop starten und warten, bis die Engine läuft.

### 1.2 Docker unter macOS installieren

1. Die [Docker-Installationsseite für macOS](https://docs.docker.com/desktop/setup/install/mac-install/) öffnen und die zum eigenen Mac passende Version herunterladen: Apple Silicon oder Intel.
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

Das Repository klonen und den Projektordner öffnen:

```text
git clone https://github.com/TutaevaIrina/hermes-ai-agent.git
cd hermes-ai-agent
```

## 3. HTW-KIWI-Zugang vorbereiten

1. Den vom Professor bereitgestellten API-Schlüssel bereithalten.
2. Den Schlüssel bei der Einrichtung in Abschnitt 5 lokal eingeben. API-Schlüssel nicht in das Git-Repository übernehmen.

### Gemeinsame Konfiguration

| Einstellung | Wert |
| --- | --- |
| API base URL | `https://f2ki-h100-1.f2.htw-berlin.de:11435/v1` |
| API-Verfahren | Chat Completions |
| Modell-ID | `qwen3.8-27b` |
| Anzeigename | `HTW KIWI` |

Die Angaben stammen aus dem vom Professor bereitgestellten Python-Beispiel `kiwi.py`. Dort wird der API-Schlüssel über die Umgebungsvariable `KIWI_API_KEY` aus einer `.env`-Datei geladen.

Für die Einrichtung über das Hermes-Menü muss dieses Python-Beispiel nicht ausgeführt werden. Die beiliegende `.env`-Datei muss für diesen Weg nicht in den Container kopiert werden; der Schlüssel wird direkt im Menü eingegeben.

**Nutzungslimits:** Für diesen HTW-Zugang liegen uns noch keine bestätigten Angaben zu Anfrage-, Token- oder Tageslimits vor. Die bisherigen Groq-Limits gelten für diesen Endpunkt nicht.

Eine Agentenaufgabe kann mehrere Modellanfragen auslösen. Auch Systemtext, Werkzeugbeschreibungen und bisherige Nachrichten benötigen Tokens. Daher starten wir mit kurzen Aufgaben und wenigen Werkzeugen.

## 4. Hermes-Image herunterladen und Daten-Volume anlegen

Die folgenden Befehle funktionieren in PowerShell sowie im macOS-/Linux-Terminal:

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

## 5. HTW KIWI und das Modell in Hermes einrichten

### 5.1 Modellauswahl öffnen

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable model
```

Wenn zunächst eine Anbieterliste erscheint, **Custom / OpenAI-compatible endpoint** oder die sinngleiche Option auswählen. Menünamen können je nach Version abweichen. Falls bereits Groq eingerichtet ist, einen benutzerdefinierten Endpunkt für HTW KIWI hinzufügen beziehungsweise den aktiven Zugang entsprechend ändern.

**API base URL:**

```text
https://f2ki-h100-1.f2.htw-berlin.de:11435/v1
```

**API key:**

Den vom Professor erhaltenen KIWI-API-Schlüssel eingeben. Eine verdeckte oder aus Sternchen bestehende Anzeige ist normal.

**Select API compatibility mode:**

```text
2. Chat Completions
```

`2` ist die Nummer im bisher beobachteten Menü. Wenn sich die Reihenfolge ändert, die Option anhand des Textes `Chat Completions` auswählen.

**Select model:**

```text
qwen3.8-27b
```

Den Modellnamen eingeben oder den passenden Listeneintrag auswählen. Die genaue Modell-ID aus dem Python-Beispiel verwenden; keinen zusätzlichen Anbieterpräfix ergänzen.

**Context length in tokens [leave blank for auto-detect]:**

Ohne Eingabe **Enter** drücken. Damit wird die automatische Ermittlung verwendet. Eine vom HTW-Server tatsächlich unterstützte Kontextgröße wurde uns bisher nicht mitgeteilt.

**Display name:**

```text
HTW KIWI
```

**Select reasoning effort:**

Falls diese Abfrage erscheint, zunächst `medium` als Starteinstellung auswählen. Das ist keine bestätigte Vorgabe für den HTW-Server. Ob der Endpunkt diese Einstellung akzeptiert, muss beim ersten Test geprüft werden; eine bisherige Groq-Einstellung wie `low` nicht ungeprüft übernehmen.

Für diesen Einstieg müssen weder Telegram noch Discord eingerichtet werden. Eine zusätzliche kostenpflichtige Anbieteranbindung ist für den beschriebenen KIWI-Zugang nicht vorgesehen.

Nach dem Speichern zum Host-Terminal zurückkehren. Eine angezeigte Modell-ID allein bestätigt noch keine funktionierende Anbieteranbindung; entscheidend ist später die erfolgreiche erste Antwort.

### 5.2 Terminal-Backend festlegen

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable config set terminal.backend local
```

**Warum `local`?** Hermes läuft bereits in einem Docker-Container. Sein lokales Terminal arbeitet deshalb innerhalb dieses Containers. Ein zusätzliches Docker-Terminal-Backend wäre ein anderer Aufbau.

Anbieter- und Modelleinstellungen lassen sich später mit dem Befehl aus Abschnitt 5.1 erneut ändern. Ein Eintrag `KIWI_API_KEY=...` in einer Datei auf dem eigenen Rechner konfiguriert Hermes nicht automatisch; diese Anleitung verwendet die Eingabe über das Hermes-Menü.

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

> Antworte kurz auf Deutsch: Was ist die Hauptstadt von Deutschland?

Es sollte eine Antwort mit `Berlin` erscheinen. Für die tatsächlich konfigurierte Modell-ID zusätzlich die Startanzeige beziehungsweise `/model` betrachten. Dort muss `qwen3.8-27b` mit dem HTW-KIWI-Endpunkt konfiguriert sein; eine Selbstauskunft des Modells ist kein verlässlicher Konfigurationsnachweis.

### 6.3 Werkzeug- und Dateitest

Anschließend diese Aufgabe eingeben:

> Lege das Verzeichnis /opt/data/team-tests an. Erstelle darin die Datei hermes-test.txt mit genau dem Inhalt „Hallo Team“. Lies die Datei anschließend mit einem Werkzeug wieder ein und zeige mir den gelesenen Inhalt sowie den vollständigen Dateipfad.

**Erwartet wird:**

- Eine echte Datei unter `/opt/data/team-tests/hermes-test.txt`.
- Eine sichtbare Werkzeugaktion, beispielsweise über Terminal oder Dateifunktionen.
- Eine Antwort mit dem Inhalt `Hallo Team`.
- Keine bloße Beschreibung, wie man die Datei selbst erstellen könnte.

Falls Hermes eine Bestätigung für die konkrete Aktion verlangt, die angezeigte Aktion lesen und passend zum Test beantworten.

Dieser Test prüft auch, ob der HTW-Endpunkt die für Hermes erforderlichen Werkzeugaufrufe unterstützt. Das bereitgestellte Python-Beispiel enthält nur eine Textanfrage und bestätigt diese Fähigkeit noch nicht.

### 6.4 Ergebnis unabhängig prüfen

Den Chat mit `/quit` beenden. Anschließend im Host-Terminal ausführen:

```text
docker run --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable bash -lc "cat /opt/data/team-tests/hermes-test.txt"
```

Es sollte `Hallo Team` ausgegeben werden. Diese Prüfung liest die Datei direkt und benötigt keine Modellanfrage.

Der neue Container kann die Datei sehen, weil sie im Volume liegt. Eine Datei unter `/tmp` wäre dafür kein geeigneter Persistenztest.

Optional dieselbe Prüfung nach einem weiteren Hermes-Start wiederholen. Falls der Start mit `bash` in einer abweichenden Image-Version anders behandelt wird, die unterstützten Aufrufmuster der offiziellen Docker-Anleitung prüfen.

