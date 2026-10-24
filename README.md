# Hermes AI Agent – Installation und erster Teamtest

Diese Anleitung richtet Hermes Agent von Nous Research in Docker ein. Sie führt von einem Rechner ohne Docker bis zu einem ersten nachvollziehbaren Agententest. Die Einrichtung ist für Windows, macOS und Linux beschrieben.

**Projektziel:** Wir untersuchen, welche Aufgaben Hermes mit einem Sprachmodell und Werkzeugen selbstständig bearbeiten kann. Für den Einstieg verwenden wir Groq als Modellanbieter und `openai/gpt-oss-120b` als Modell.

**Stand:** 22. Oktober 2026. Menüs, verfügbare Modelle und kostenlose Kontingente können sich ändern. Auswahltexte und Modellnamen sind wichtiger als Menünummern.

> Jedes Teammitglied führt die Einrichtung auf dem eigenen Rechner mit einem eigenen API-Schlüssel durch. Das Repository enthält die gemeinsame Anleitung und Testergebnisse; die persönliche Hermes-Konfiguration liegt in einem lokalen Docker-Volume.

## Inhalt

1. [Überblick und Voraussetzungen](#1-überblick-und-voraussetzungen)
2. [Docker unter Windows installieren](#2-docker-unter-windows-installieren)
3. [Docker unter macOS installieren](#3-docker-unter-macos-installieren)
4. [Docker unter Linux installieren](#4-docker-unter-linux-installieren)
5. [Docker prüfen und Projektordner öffnen](#5-docker-prüfen-und-projektordner-öffnen)
6. [Groq-Zugang vorbereiten](#6-groq-zugang-vorbereiten)
7. [Hermes-Image herunterladen und Daten-Volume anlegen](#7-hermes-image-herunterladen-und-daten-volume-anlegen)
8. [Groq und das Modell in Hermes einrichten](#8-groq-und-das-modell-in-hermes-einrichten)
9. [Hermes starten und den ersten Test durchführen](#9-hermes-starten-und-den-ersten-test-durchführen)
10. [Optional: lokalen Testordner bereitstellen](#10-optional-lokalen-testordner-bereitstellen)
11. [Ergebnisse im Team dokumentieren](#11-ergebnisse-im-team-dokumentieren)
12. [Alltag: Neustart, Diagnose und Updates](#12-alltag-neustart-diagnose-und-updates)
13. [Häufige Fehler beheben](#13-häufige-fehler-beheben)
14. [Offizielle Quellen und Prüfumfang](#14-offizielle-quellen-und-prüfumfang)

## 1. Überblick und Voraussetzungen

### Was wird wo ausgeführt?

| Bestandteil | Aufgabe | Ort |
| --- | --- | --- |
| Docker Desktop bzw. Docker Engine | Startet und verwaltet Container | Eigener Rechner |
| Hermes Agent | Plant Schritte und nutzt Werkzeuge | Docker-Container |
| Groq | Führt das ausgewählte Sprachmodell aus | Externer API-Dienst |
| `hermes-test-data` | Bewahrt persönliche Einstellungen und Hermes-Daten auf | Lokales Docker-Volume |
| Optionaler Ordner `workspace` | Stellt Testdateien bereit und nimmt Ergebnisse auf | Projektordner, im Container unter `/work` erreichbar |

Das Modell läuft bei diesem Aufbau bei Groq. Auf dem eigenen Rechner muss dafür weder das Modell heruntergeladen noch eine leistungsfähige Grafikkarte vorhanden sein. Prompts und die an das Modell übergebenen Dateiinhalte werden an den API-Anbieter gesendet. Für erste Versuche verwenden wir selbst erstellte Beispieldaten.

Ein **Image** ist die vorbereitete Softwarevorlage. `docker pull` lädt sie herunter. `docker run` startet daraus einen **Container**. Ein **Volume** speichert Daten unabhängig von einem einzelnen Container.

### Benötigt werden

- Eine Internetverbindung für Downloads und Modellanfragen.
- Ein für Docker unterstütztes Betriebssystem und genügend freier Speicher für das Image.
- Unter Windows und macOS: Docker Desktop.
- Unter Linux: Docker Engine; Beispiele für Ubuntu, Debian und Fedora folgen unten.
- Ein Groq-Konto mit aktivem API-Schlüssel und Zugang zum ausgewählten Modell.
- Ein Terminal: PowerShell unter Windows, Terminal unter macOS, Bash unter Linux.

Für die hier verwendeten Startbefehle ist keine lokale Python- oder Node.js-Installation nötig. Docker Compose wird bei den beschriebenen Installationswegen mitinstalliert, ist für den Start mit `docker run` aber optional.

**Kosten:** Docker Desktop ist unter anderem für persönliche Nutzung und Bildung kostenlos. Für bestimmte berufliche Nutzungen ist eine Lizenz erforderlich. Die aktuellen [Docker-Desktop-Lizenzbedingungen](https://docs.docker.com/subscription-billing/desktop-license/) sind maßgeblich. Groqs Free Plan hat eigene Kontingente; „kostenlos“ bedeutet keine unbegrenzte Nutzung.

## 2. Docker unter Windows installieren

Bereits installiert? Direkt zu [Abschnitt 5](#5-docker-prüfen-und-projektordner-öffnen) gehen.

### 2.1 Voraussetzungen prüfen

Für diese Anleitung verwenden wir Docker Desktop mit WSL 2 und Linux-Containern.

1. Die aktuelle [Windows-Installationsseite von Docker](https://docs.docker.com/desktop/setup/install/windows-install/) öffnen und prüfen, ob die eigene Windows-Version unterstützt wird.
2. Im Task-Manager unter **Leistung → CPU** nach **Virtualisierung: Aktiviert** schauen. Bei deaktivierter Virtualisierung muss sie gegebenenfalls im BIOS/UEFI eingeschaltet werden.
3. Für den WSL-2-Weg nennt Docker derzeit unter anderem 8 GB Arbeitsspeicher und WSL ab Version 2.1.5. Die verlinkte Seite enthält die vollständigen Anforderungen.

### 2.2 WSL prüfen oder installieren

PowerShell öffnen und ausführen:

```powershell
wsl --version
wsl --status
```

Wenn WSL fehlt, PowerShell **als Administrator** öffnen:

```powershell
wsl --install
```

Den Rechner bei Aufforderung neu starten. Falls die installierte Linux-Distribution beim ersten Start einen Benutzernamen und ein Passwort verlangt, diese Einrichtung abschließen.

Danach WSL aktualisieren und WSL 2 als Standard für neue Distributionen setzen:

```powershell
wsl --update
wsl --set-default-version 2
wsl --list --verbose
```

Bei einer bereits vorhandenen Distribution mit Version 1 diese gemäß [Microsofts WSL-Anleitung](https://learn.microsoft.com/en-us/windows/wsl/install) auf Version 2 umstellen. Der Distributionsname muss dabei dem eigenen Eintrag entsprechen.

### 2.3 Docker Desktop installieren

1. [Docker Desktop für Windows](https://docs.docker.com/desktop/setup/install/windows-install/) öffnen.
2. Den zum Prozessor passenden Installer herunterladen: bei üblichen Intel-/AMD-PCs **x86_64**, bei Windows-on-Arm den dafür angebotenen Installer.
3. Installer ausführen und die Installation abschließen.
4. Wenn nach dem Backend gefragt wird, **WSL 2** verwenden.
5. Eventuelle Neustartaufforderungen ausführen.
6. Docker Desktop über das Startmenü starten und warten, bis die Engine läuft.
7. In den Einstellungen bei Bedarf **General → Use the WSL 2 based engine** prüfen. Die genaue Menübezeichnung kann je nach Version variieren.
8. **Linux-Container** verwenden, da das Hermes-Image ein Linux-Image ist.

Falls die Docker-Oberfläche einen Anmeldebildschirm zeigt, die für die eigene Nutzung angebotenen Optionen beachten. Für Groq ist später ein separates Konto nötig.

PowerShell nach der Installation neu öffnen und mit Abschnitt 5 fortfahren. Die folgenden Windows-Befehle werden in **PowerShell auf Windows** ausgeführt; ein zusätzlich in WSL installiertes Docker Engine ist für diesen Weg nicht nötig.

## 3. Docker unter macOS installieren

Bereits installiert? Direkt zu Abschnitt 5 gehen.

1. Unter **Apple-Menü → Über diesen Mac** nachsehen, ob der Rechner einen Apple-Chip oder einen Intel-Prozessor hat.
2. Die [Docker-Installationsseite für macOS](https://docs.docker.com/desktop/setup/install/mac-install/) öffnen.
3. Das passende Paket auswählen:
   - **Apple silicon** für Macs mit Apple-Chip.
   - **Intel chip** für Intel-Macs.
4. Die heruntergeladene `.dmg` öffnen.
5. Docker in den Ordner **Programme / Applications** ziehen.
6. Docker aus **Programme** starten.
7. Die angezeigten Einrichtungsschritte abschließen und erforderliche Berechtigungen erteilen.
8. Warten, bis Docker Desktop die laufende Engine anzeigt.
9. Die App **Terminal** öffnen und mit Abschnitt 5 fortfahren.

Die aktuell unterstützten macOS-Versionen und Hardwareanforderungen stehen auf der verlinkten Docker-Seite. Für das Hermes-Image wird keine CPU-Architektur erzwungen; Docker verwendet die passende Variante, sofern sie im Image vorhanden ist.

## 4. Docker unter Linux installieren

Dieser Abschnitt beschreibt eine Installation von **Docker Engine** über die offiziellen Paketquellen. Nur den Unterabschnitt für die eigene Distribution ausführen.

Die Distribution lässt sich so prüfen:

```bash
cat /etc/os-release
```

Die Beispiele richten sich an unterstützte Ubuntu-, Debian- und Fedora-Versionen. Bei anderen Distributionen die passende [offizielle Installationsanleitung](https://docs.docker.com/engine/install/) verwenden. Ubuntu-Ableger wie Linux Mint und Debian-Ableger können zusätzliche Anpassungen benötigen.

**Bei bestehender Installation:** Wenn Docker bereits funktioniert, direkt zu Abschnitt 5 gehen. Bestehende Pakete wie `docker.io`, ältere Compose-Pakete oder `podman-docker` können mit der offiziellen Docker-Installation kollidieren. In diesem Fall zuerst die Hinweise zur Paketmigration in der jeweiligen offiziellen Anleitung lesen.

### 4.1 Ubuntu

Quelle: [Docker Engine unter Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

Paketliste aktualisieren und Hilfsprogramme installieren:

```bash
sudo apt update
sudo apt install -y ca-certificates curl
```

Schlüssel der offiziellen Docker-Paketquelle hinterlegen:

```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

Paketquelle einrichten:

```bash
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

Docker Engine, CLI, Buildx und Compose installieren:

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo docker run --rm hello-world
```

Anschließend mit Abschnitt 4.4 fortfahren.

### 4.2 Debian

Quelle: [Docker Engine unter Debian](https://docs.docker.com/engine/install/debian/).

```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

Paketquelle einrichten:

```bash
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

Pakete installieren und Dienst starten:

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo docker run --rm hello-world
```

Anschließend mit Abschnitt 4.4 fortfahren.

### 4.3 Fedora

Quelle: [Docker Engine unter Fedora](https://docs.docker.com/engine/install/fedora/). Die folgende Repository-Syntax entspricht dem aktuellen DNF5-Weg.

```bash
sudo dnf install -y dnf5-plugins
sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Bei Nachfrage den GPG-Schlüssel mit dem Fingerabdruck auf der offiziellen Docker-Seite vergleichen. Danach:

```bash
sudo systemctl enable --now docker
sudo docker run --rm hello-world
```

### 4.4 Docker-Befehle als eigener Benutzer ausführen

Die folgenden Projektbefehle sind ohne `sudo` geschrieben. Wer diesen Weg verwenden möchte, kann den eigenen Benutzer zur Docker-Gruppe hinzufügen:

```bash
sudo usermod -aG docker "$USER"
```

Danach **vollständig abmelden und wieder anmelden** und ein neues Terminal öffnen. Falls die Gruppe fehlt, zuvor mit `sudo groupadd docker` anlegen.

Die Docker-Gruppe gewährt weitreichende, rootähnliche Rechte. Alternativ kann Docker mit `sudo` verwendet oder nach der offiziellen Anleitung im Rootless-Modus eingerichtet werden. Bei Verwendung mit `sudo` muss es vor den folgenden `docker`-Befehlen ergänzt werden.

Quelle: [Linux-Nachinstallation und Benutzerrechte](https://docs.docker.com/engine/install/linux-postinstall/).

## 5. Docker prüfen und Projektordner öffnen

### 5.1 Installation überprüfen

Diese Befehle funktionieren in PowerShell sowie im macOS-/Linux-Terminal:

```text
docker --version
docker version
docker info
docker run --rm hello-world
```

**Erwartetes Ergebnis:**

- `docker --version` zeigt die installierte CLI-Version.
- `docker version` zeigt **Client und Server**.
- `docker info` liefert Informationen zur erreichbaren Engine.
- Der Testcontainer gibt eine Erfolgsmeldung mit `Hello from Docker!` aus.

Nur eine erfolgreiche Ausgabe von `docker --version` reicht nicht: Sie bestätigt allein, dass das Kommando installiert ist.

Optional Compose prüfen:

```text
docker compose version
```

### 5.2 Repository lokal bereitstellen

Das gemeinsame Repository klonen oder über die Repository-Oberfläche als ZIP herunterladen und entpacken. Beim Klonen den folgenden Platzhalter durch die echte Repository-URL ersetzen:

```text
git clone <REPOSITORY-URL> hermes-ai-agent
cd hermes-ai-agent
```

`<REPOSITORY-URL>` ist ein Platzhalter und darf nicht unverändert ausgeführt werden. Zum Klonen muss Git installiert sein; beim ZIP-Weg wird Git für die Installation nicht benötigt.

Bei einem bereits vorhandenen Projektordner diesen öffnen.

**Windows / PowerShell – Beispiel:**

```powershell
Set-Location "C:\Users\irina\Documents\Software Projects\hermes-ai-agent"
```

Andere Teammitglieder ersetzen den Pfad durch ihren eigenen Projektpfad. Anführungszeichen sind bei Leerzeichen nötig.

**macOS / Linux – Beispiel:**

```bash
cd "$HOME/Documents/hermes-ai-agent"
```

Der Ordner muss bereits existieren. Das Wechseln in den Repository-Ordner macht dessen Dateien noch nicht im Container sichtbar. Ein optionaler Dateiaustausch wird in Abschnitt 10 eingerichtet.

## 6. Groq-Zugang vorbereiten

1. [Groq Console](https://console.groq.com/) öffnen.
2. Ein eigenes Konto erstellen oder anmelden.
3. Unter [API Keys](https://console.groq.com/keys) einen API-Schlüssel anlegen.
4. Den Schlüssel für die anschließende lokale Eingabe bereithalten.
5. Unter [Limits](https://console.groq.com/settings/limits) das verfügbare Kontingent des eigenen Kontos prüfen.

Jede Person verwendet ihren eigenen Schlüssel. Schlüssel gehören weder in diese README noch in Git-Commits, geteilte Screenshots oder Testprotokolle. Falls ein Schlüssel veröffentlicht wurde, ihn in der Groq Console widerrufen und ersetzen.

### Gemeinsame Konfiguration

| Einstellung | Wert für den Einstieg |
| --- | --- |
| API-Anbieter | Groq über einen benutzerdefinierten OpenAI-kompatiblen Zugang |
| API-Basisadresse | `https://api.groq.com/openai/v1` |
| API-Modus | `Chat Completions` |
| Modell-ID | `openai/gpt-oss-120b` |
| Kontextlänge | Automatisch erkennen lassen |
| Anzeigename | `Groq` |
| Reasoning effort / Denkaufwand | `low` |
| Terminal-Backend | `local` innerhalb des Hermes-Containers |
| Werkzeuge für den ersten Test | `terminal,file` |

`openai/gpt-oss-120b` unterstützt Werkzeugaufrufe. Trotz des Modellnamens wird es hier über **Groq** angesprochen; für diesen Weg ist ein Groq-Schlüssel erforderlich.

**Kostenlose Grenzen, Stand 22.10.2026:** Die öffentliche Groq-Tabelle nennt für dieses Modell im Free Plan 30 Anfragen pro Minute, 1.000 pro Tag, 8.000 Tokens pro Minute und 200.000 Tokens pro Tag. Die Werte im eigenen Konto sind maßgeblich.

Eine Agentenaufgabe kann mehrere Modellanfragen auslösen. Auch Systemtext, Werkzeugbeschreibungen und bisherige Nachrichten benötigen Tokens. Ein großes Kontextfenster hebt das Tokenlimit pro Minute nicht auf. Daher starten wir mit kurzen Aufgaben und wenigen Werkzeugen.

Quellen: [Groq Quickstart](https://console.groq.com/docs/quickstart), [OpenAI-Kompatibilität](https://console.groq.com/docs/openai), [Modellbeschreibung](https://console.groq.com/docs/model/openai/gpt-oss-120b), [Rate Limits](https://console.groq.com/docs/rate-limits).

## 7. Hermes-Image herunterladen und Daten-Volume anlegen

Die folgenden Befehle gelten für alle drei Betriebssysteme:

```text
docker pull nousresearch/hermes-agent:stable
docker volume create hermes-test-data
```

`pull` lädt das fertige Hermes-Image herunter. Beim ersten Download kann das einige Zeit dauern. Das Volume wird einmal angelegt; ein erneuter Aufruf mit demselben Namen verwendet das vorhandene Volume.

Prüfen:

```text
docker image ls nousresearch/hermes-agent
docker volume inspect hermes-test-data
```

Das Volume wird später unter `/opt/data` eingebunden. Es hält persönliche Konfiguration, Zugangsdaten und Hermes-Zustand über Containerstarts hinweg vor. Auf jedem Rechner ist `hermes-test-data` ein eigenes lokales Volume; derselbe Name synchronisiert keine Daten zwischen Teammitgliedern.

Das offizielle Image ist bereits vorbereitet. Ein eigener Dockerfile-Build ist für diesen Einstieg nicht nötig.

Quelle: [Hermes in Docker](https://hermes-agent.nousresearch.com/docs/user-guide/docker).

## 8. Groq und das Modell in Hermes einrichten

### 8.1 Modellauswahl öffnen

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable model
```

Der Aufruf führt den Hermes-Unterbefehl `model` im Container aus.

| Argument | Bedeutung |
| --- | --- |
| `-it` | Ermöglicht interaktive Eingaben im Terminal |
| `--rm` | Entfernt den beendeten Container automatisch |
| `-v hermes-test-data:/opt/data` | Verbindet das dauerhafte Daten-Volume mit Hermes |
| `nousresearch/hermes-agent:stable` | Verwendetes Image |
| `model` | Öffnet die Anbieter- und Modellkonfiguration |

Das Volume bleibt bei `--rm` erhalten.

### 8.2 Alle Auswahlfelder ausfüllen

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

### 8.3 Terminal-Backend festlegen

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable config set terminal.backend local
```

**Warum `local`?** Hermes läuft bereits in einem Docker-Container. Sein lokales Terminal arbeitet deshalb innerhalb dieses Containers. Ein zusätzliches Docker-Terminal-Backend wäre ein anderer Aufbau.

Anbieter- und Modelleinstellungen lassen sich später mit dem Befehl aus Abschnitt 8.1 erneut ändern. Ein eigener Eintrag `GROQ_MODEL=...` aus einem früheren Python-Projekt konfiguriert Hermes nicht automatisch.

Quellen: [Hermes-Modellanbieter](https://hermes-agent.nousresearch.com/docs/integrations/providers), [Hermes-Konfiguration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration).

## 9. Hermes starten und den ersten Test durchführen

### 9.1 Chat mit wenigen Werkzeugen starten

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable chat --toolsets "terminal,file"
```

Die Werkzeugauswahl begrenzt den ersten Versuch auf Terminal und Dateibearbeitung. Das reduziert zugleich den Umfang der Werkzeugbeschreibungen im Modellkontext.

Im Chat werden normale Aufgaben eingegeben. Docker-Befehle aus dieser Anleitung dagegen gehören in das Terminal des eigenen Rechners.

### 9.2 Verbindungstest

Zunächst eingeben:

> Antworte kurz auf Deutsch: Welches Modell wird in dieser Sitzung verwendet?

Für die tatsächlich konfigurierte Modell-ID zusätzlich die Startanzeige bzw. `/model` betrachten; eine Selbstauskunft des Modells ist kein verlässlicher Konfigurationsnachweis.

### 9.3 Werkzeug- und Dateitest

Anschließend diese Aufgabe eingeben:

> Lege das Verzeichnis /opt/data/team-tests an. Erstelle darin die Datei hermes-test.txt mit genau dem Inhalt „Hallo Team“. Lies die Datei anschließend mit einem Werkzeug wieder ein und zeige mir den gelesenen Inhalt sowie den vollständigen Dateipfad.

**Erwartet wird:**

- Eine echte Datei unter `/opt/data/team-tests/hermes-test.txt`.
- Eine sichtbare Werkzeugaktion, beispielsweise über Terminal oder Dateifunktionen.
- Eine Antwort mit dem Inhalt `Hallo Team`.
- Keine bloße Beschreibung, wie man die Datei selbst erstellen könnte.

Falls Hermes eine Bestätigung für die konkrete Aktion verlangt, die angezeigte Aktion lesen und passend zum Test beantworten.

### 9.4 Ergebnis unabhängig prüfen

Den Chat mit `/quit` beenden. Anschließend im Host-Terminal ausführen:

```text
docker run --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable bash -lc "cat /opt/data/team-tests/hermes-test.txt"
```

Es sollte `Hallo Team` ausgegeben werden. Diese Prüfung liest die Datei direkt und benötigt keine Modellanfrage.

Der neue Container kann die Datei sehen, weil sie im Volume liegt. Eine Datei unter `/tmp` wäre dafür kein geeigneter Persistenztest.

Optional dieselbe Prüfung nach einem weiteren Hermes-Start wiederholen. Falls der Start mit `bash` in einer abweichenden Image-Version anders behandelt wird, die unterstützten Aufrufmuster der offiziellen Docker-Anleitung prüfen.

### 9.5 Erfolgskriterien

| Prüfung | Erfolgskriterium |
| --- | --- |
| Docker | Client und Server sind erreichbar; `hello-world` funktioniert |
| API-Zugang | Hermes erhält eine Modellantwort |
| Modellkonfiguration | `openai/gpt-oss-120b` wird als gewähltes Modell angezeigt |
| Werkzeuge | Die Datei wird tatsächlich erstellt und eingelesen |
| Persistenz | Ein neu gestarteter Container kann dieselbe Datei lesen |

Quelle für Werkzeugauswahl und CLI: [Tools & Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools), [CLI Interface](https://hermes-agent.nousresearch.com/docs/user-guide/cli).

## 10. Optional: lokalen Testordner bereitstellen

Der erste Test braucht keinen Zugriff auf lokale Repository-Dateien. Für eigene CSV-Dateien oder sichtbare Ergebnisdateien kann ein Unterordner `workspace` zusätzlich eingebunden werden.

Dann gilt diese Zuordnung:

| Auf dem eigenen Rechner | Im Container |
| --- | --- |
| `<Projektordner>/workspace` | `/work` |
| `<Projektordner>/workspace/auswertung.txt` | `/work/auswertung.txt` |
| Docker-Volume `hermes-test-data` | `/opt/data` |

`workspace` enthält die Testdateien. Die persönliche Hermes-Konfiguration bleibt weiterhin im Volume.

### Windows / PowerShell

Im Projektordner ausführen:

```powershell
New-Item -ItemType Directory -Force -Path ".\workspace" | Out-Null
$hermesWorkspace = (Resolve-Path ".\workspace").Path
docker run -it --rm -v hermes-test-data:/opt/data --mount "type=bind,source=$hermesWorkspace,target=/work" nousresearch/hermes-agent:stable chat --toolsets "terminal,file"
```

Die Variable muss in derselben PowerShell-Sitzung gesetzt sein, in der der Start erfolgt.

### macOS

Im Projektordner ausführen:

```bash
mkdir -p workspace
docker run -it --rm -v hermes-test-data:/opt/data --mount "type=bind,source=$(pwd)/workspace,target=/work" nousresearch/hermes-agent:stable chat --toolsets "terminal,file"
```

Bei einem Hinweis auf Dateifreigaben den Projektordner in Docker Desktop für den Containerzugriff freigeben.

### Linux

Im Projektordner ausführen. Bei einer normalen Installation als eigener Benutzer passen die UID-/GID-Variablen den Hermes-Laufzeitbenutzer an den Besitzer des Testordners an:

```bash
mkdir -p workspace
docker run -it --rm -e HERMES_UID="$(id -u)" -e HERMES_GID="$(id -g)" -v hermes-test-data:/opt/data --mount "type=bind,source=$(pwd)/workspace,target=/work" nousresearch/hermes-agent:stable chat --toolsets "terminal,file"
```

Bei aktiviertem SELinux, etwa unter Fedora, kann ein eigenes Label für diesen dedizierten Testordner erforderlich sein. Dafür statt `--mount` den folgenden `-v`-Aufruf verwenden:

```bash
docker run -it --rm -e HERMES_UID="$(id -u)" -e HERMES_GID="$(id -g)" -v hermes-test-data:/opt/data -v "$(pwd)/workspace:/work:Z" nousresearch/hermes-agent:stable chat --toolsets "terminal,file"
```

`:Z` ist für diesen eigenen Testordner gedacht, da Docker dessen SELinux-Label ändert. Bei Rootless Docker oder angepasstem User-Namespace können andere Rechtezuordnungen nötig sein; bei Problemen zunächst den Test ausschließlich im Volume aus Abschnitt 9 verwenden.

### Lokalen Dateiaustausch prüfen

Im Hermes-Chat eingeben:

> Erstelle die Datei /work/team-ergebnis.txt mit dem Inhalt „Der Dateiaustausch funktioniert“. Lies sie wieder ein und zeige den Inhalt.

Danach sollte `workspace/team-ergebnis.txt` auch im Dateimanager auf dem eigenen Rechner sichtbar sein.

Ein beschreibbarer Mount erlaubt Änderungen an genau diesem freigegebenen Ordner. Für die Tests nur die benötigten Dateien darin ablegen.

Quellen: [Docker Bind Mounts](https://docs.docker.com/engine/storage/bind-mounts/), [Benutzerzuordnung im Hermes-Image](https://hermes-agent.nousresearch.com/docs/user-guide/docker).

## 11. Ergebnisse im Team dokumentieren

Damit sich Ergebnisse vergleichen lassen, sollte das Team zunächst dieselbe Modell-ID, denselben Denkaufwand, dieselben Werkzeuge und dieselben Testaufgaben verwenden. Modellverhalten und Antwortqualität können trotzdem schwanken.

### Vorlage für ein Testprotokoll

| Feld | Eintrag |
| --- | --- |
| Datum und testende Person | |
| Betriebssystem und Architektur | |
| Docker-Version | |
| Hermes-Image-Tag und Digest | |
| Anbieter / Modell | `Groq / openai/gpt-oss-120b` |
| Reasoning effort | `low` |
| Aktivierte Toolsets | `terminal,file` |
| Neue oder fortgesetzte Sitzung | |
| Genaue Aufgabe | |
| Erwartetes Ergebnis | |
| Beobachtetes Ergebnis und Werkzeugaktionen | |
| Manuelle Eingriffe / Rückfragen | |
| Dauer und API-Verbrauch, falls verfügbar | |
| Bewertung | Erfolgreich / teilweise erfolgreich / fehlgeschlagen |

Das Protokoll enthält keine API-Schlüssel. Bestehende Erinnerungen und vorherige Gespräche können Ergebnisse beeinflussen und sollten bei Vergleichstests berücksichtigt werden.

Die ersten Aufgaben können sein:

1. Eine Datei erstellen, lesen und nach einem Containerneustart wiederfinden.
2. Eine kleine, selbst erstellte CSV zusammenfassen und die berechneten Werte nachprüfen.
3. Ein kurzes fehlerhaftes Skript untersuchen, korrigieren und ausführen.
4. Eine mehrstufige Aufgabe mit klaren Erfolgskriterien bearbeiten.

Webrecherche, Browserbedienung und weitere Integrationen kommen erst später hinzu. Ein funktionierender Modellschlüssel konfiguriert nicht automatisch alle externen Werkzeuge.

### Hinweise für das Repository

Gemeinsam versioniert werden beispielsweise diese README, harmlose Eingabedateien und bereinigte Testberichte. Persönliche Zugangsdaten und vollständige Hermes-Daten werden nicht eingecheckt.

Falls später lokale Konfigurations- oder Exportdateien entstehen, können folgende Einträge in eine vorhandene `.gitignore` ergänzt werden:

```gitignore
.env
.env.*
!.env.example
.hermes/
hermes-data/
backups/
```

Vorhandene `.gitignore`-Einträge beibehalten. Eine ignorierte Datei, die bereits in Git erfasst ist, bleibt weiterhin erfasst. Das Docker-Volume selbst liegt außerhalb des Repository-Arbeitsbaums.

## 12. Alltag: Neustart, Diagnose und Updates

### Erneut starten

Docker Desktop bzw. Docker Engine muss laufen. Danach:

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable chat --toolsets "terminal,file"
```

Die Anbieter-Einrichtung muss mit demselben Volume nicht bei jedem Start wiederholt werden. Für den lokalen Dateiaustausch den passenden Startbefehl aus Abschnitt 10 verwenden.

### Beenden

Im Chat `/quit` eingeben. Anschließend erscheint wieder das Host-Terminal. Der Container wird durch `--rm` entfernt; das benannte Volume bleibt bestehen.

### Diagnose und Hilfe

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable doctor
docker run --rm nousresearch/hermes-agent:stable --help
```

Für eine Diagnose zu einem laufenden Problem den Chat zuerst beenden. Bei geteilten Diagnoseausgaben mögliche Zugangsdaten und persönliche Inhalte entfernen.

Werkzeugauswahl bei Bedarf interaktiv prüfen:

```text
docker run -it --rm -v hermes-test-data:/opt/data nousresearch/hermes-agent:stable tools
```

### Image-Version dokumentieren

`stable` ist ein veränderlicher Tag. Er kann bei einem späteren Download auf eine andere Veröffentlichung zeigen.

```text
docker image inspect nousresearch/hermes-agent:stable --format '{{index .RepoDigests 0}}'
```

Den ausgegebenen Image-Verweis im Testprotokoll festhalten. Für festgelegte Vergleichsläufe kann das Team einen passenden versionierten Tag oder Digest vereinbaren und ihn in allen Befehlen anstelle von `:stable` verwenden. Bei gemischten Intel-/AMD- und Arm-Rechnern muss der gewählte Verweis die benötigten Architekturen unterstützen.

### Aktualisieren

1. Laufende Hermes-Sitzung beenden.
2. Vor einem wichtigen Vergleichslauf gemeinsam entscheiden, ob die Version geändert werden soll.
3. Neues Image herunterladen:

```text
docker pull nousresearch/hermes-agent:stable
```

4. Hermes mit dem gewohnten Startbefehl neu starten und den Dateitest wiederholen.
5. Den neuen Digest im Protokoll festhalten.

Bei diesem Aufbau wird Hermes durch ein neues Image aktualisiert. Das vorhandene Daten-Volume wird erneut eingebunden. Image-Updates ersetzen keine Datensicherung.

Es gibt hier keinen Schritt zum Löschen des Daten-Volumes: Darin liegen die persönliche Konfiguration und Testergebnisse.

## 13. Häufige Fehler beheben

| Meldung / Beobachtung | Bedeutung und nächster Schritt |
| --- | --- |
| `docker` wird nicht erkannt | Installation abschließen und Terminal neu öffnen; unter Windows/macOS Docker Desktop prüfen. |
| `Cannot connect to the Docker daemon` oder Docker-Desktop-Pipe nicht gefunden | Docker Desktop starten bzw. unter Linux `sudo systemctl start docker` ausführen; anschließend `docker info` prüfen. |
| `permission denied` am Docker-Socket | Unter Linux Gruppenmitgliedschaft prüfen und neu anmelden oder die Docker-Befehle mit `sudo` ausführen. |
| WSL- oder Virtualisierungsfehler | `wsl --update` ausführen, Neustart und BIOS/UEFI-Virtualisierung prüfen; offizielle WSL-/Docker-Anforderungen beachten. |
| `no matching manifest` / falsche Containerplattform | Linux-Container verwenden, Prozessorarchitektur prüfen und das unterstützte Image ohne erzwungenes `--platform` erneut laden. |
| Registry-Download scheitert | Internet, Proxy und Registry-Erreichbarkeit prüfen; bei Docker-Hub-Limits den Hinweis zur Anmeldung oder Wartezeit beachten. |
| `401` / `invalid_api_key` | In der Groq Console prüfen, ob der eigene Schlüssel aktiv ist; Modellkonfiguration aus Abschnitt 8 erneut öffnen. |
| `403` oder Modellzugriff verweigert | Modellberechtigung und Kontozugang bei Groq prüfen. Ein gültiger Schlüssel garantiert nicht Zugriff auf jedes Modell. |
| `429` / `rate_limit_exceeded` | Betroffenes Minuten- oder Tageslimit in der Meldung und im Groq-Konto prüfen. Bei Minutenlimits warten; bei Tageslimits auf den Reset warten. |
| Schon die erste Aufgabe überschreitet das Tokenlimit | Mit `--toolsets "terminal,file"` starten, unnötige Werkzeuge und lange Inhalte reduzieren. Eine einzelne zu große Anfrage wird durch Warten allein nicht kleiner. |
| `model_not_found` / `model_decommissioned` | Modellnamen und aktuelle Groq-Modellliste prüfen; im Team einen verfügbaren Ersatz festlegen. |
| `unsupported parameter` / Reasoning-Fehler | Groq-Modell und API-Modus prüfen. Eine für das Modell unterstützte Reasoning-Stufe wie `low` verwenden. |
| Hermes behauptet, eine Datei erstellt zu haben | Dateipfad und Werkzeugprotokoll prüfen; mit dem direkten `cat`-Befehl aus Abschnitt 9 unabhängig nachsehen. |
| Testdatei nach Neustart weg | Lag sie unter `/tmp` oder außerhalb der eingebundenen Verzeichnisse? Dauerhafte Testdateien unter `/opt/data/team-tests` oder `/work` ablegen. |
| Anbieter nach jedem Start wieder unkonfiguriert | Bei jedem Befehl genau `-v hermes-test-data:/opt/data` verwenden und prüfen, ob derselbe Docker-Kontext aktiv ist. |
| `invalid mount config` / Quellordner fehlt | `workspace` zuerst anlegen, richtigen Projektordner öffnen und den vollständigen Pfad wie in Abschnitt 10 angeben. |
| `Permission denied` beim Schreiben nach `/work` | Host-Ordnerrechte prüfen; unter Linux UID/GID und gegebenenfalls SELinux berücksichtigen. |
| `OOMKilled` / Exit-Code `137` | Speicherbelegung prüfen und Docker mehr Arbeitsspeicher zuweisen oder die Aufgabe verkleinern. |

### Hinweise zu typischen Startausgaben

Eine Startzeile wie diese ist zunächst eine Informationsmeldung:

```text
/package/admin/s6-overlay/libexec/preinit: info: container permissions: uid=0 (root) ...
```

Sie allein zeigt keinen Fehler. Das offizielle Image nutzt beim Start administrative Schritte und kann für den eigentlichen Hermes-Prozess auf einen anderen Benutzer wechseln. Entscheidend sind nachfolgende Fehlermeldungen und die erfolgreiche Ausführung.

### Wenn die Modellliste eine andere Reihenfolge hat

Nach `openai/gpt-oss-120b` suchen bzw. die Modell-ID direkt eingeben. Keine Nummer aus einem fremden Screenshot blind übernehmen. In unserem beobachteten Menü waren auch Audio-, Schutz- und andere Spezialmodelle enthalten; diese sind nicht die vereinbarte Auswahl für den ersten Agententest.

### Wenn das kostenlose Kontingent für Hermes nicht ausreicht

Tokenlimits sind eine Grenze des verwendeten Modellzugangs und sollten im Testbericht gesondert vermerkt werden. Zunächst den Werkzeugumfang und die Aufgabengröße reduzieren. Reicht das weiterhin nicht aus, gemeinsam einen anderen verfügbaren Zugang mit Tool Calling und ausreichendem Kontext prüfen.

## 14. Offizielle Quellen und Prüfumfang

Die Befehle und Einstellungen wurden für diese README mit folgenden offiziellen Quellen abgeglichen. Diese Links sind auch die Anlaufstellen bei abweichenden Menütexten oder geänderten Anforderungen.

### Docker und Windows

- [Docker Desktop – Windows-Installation](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Microsoft – WSL installieren](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Docker Desktop – macOS-Installation](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Docker Engine – Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Docker Engine – Debian](https://docs.docker.com/engine/install/debian/)
- [Docker Engine – Fedora](https://docs.docker.com/engine/install/fedora/)
- [Docker Engine – weitere Distributionen](https://docs.docker.com/engine/install/)
- [Docker – Linux-Nachinstallation](https://docs.docker.com/engine/install/linux-postinstall/)
- [Docker – Volumes](https://docs.docker.com/engine/storage/volumes/)
- [Docker – Bind Mounts](https://docs.docker.com/engine/storage/bind-mounts/)
- [Docker Desktop – Lizenzbedingungen](https://docs.docker.com/subscription-billing/desktop-license/)

### Hermes

- [Offizielles Hermes-Repository](https://github.com/NousResearch/hermes-agent)
- [Hermes in Docker](https://hermes-agent.nousresearch.com/docs/user-guide/docker)
- [Modellanbieter](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [Konfiguration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [Werkzeuge und Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools)
- [CLI Interface](https://hermes-agent.nousresearch.com/docs/user-guide/cli)

### Groq

- [Quickstart](https://console.groq.com/docs/quickstart)
- [OpenAI-Kompatibilität](https://console.groq.com/docs/openai)
- [GPT-OSS 120B](https://console.groq.com/docs/model/openai/gpt-oss-120b)
- [Rate Limits](https://console.groq.com/docs/rate-limits)
- [Modellabkündigungen und Ersatzmodelle](https://console.groq.com/docs/deprecations)

**Prüfumfang dieser Anleitung:** Die Auswahlfelder des Groq-Setups stammen aus dem beobachteten Windows-Einrichtungsablauf. Die Installationswege und ergänzenden Befehle wurden mit der offiziellen Dokumentation abgeglichen. Ein vollständiger Lauf auf Windows, macOS und Linux sowie erfolgreiche Modell- und Dateitests sind durch das Team anhand der Erfolgskriterien in Abschnitt 9 noch zu bestätigen.

