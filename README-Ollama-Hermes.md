# Hermes AI Agent mit Ollama in Docker

**Einrichtung und erster Teamtest**

Diese Anleitung beschreibt, wie Hermes Agent in Docker mit einem lokal ausgeführten Ollama-Modell verbunden wird. Dadurch werden keine externen API-Anfragen und keine kostenlosen API-Tokenkontingente benötigt. Das Sprachmodell läuft auf dem eigenen Rechner; Hermes läuft im Docker-Container.

## 1. Voraussetzungen

Benötigt werden:

- Docker Desktop mit Linux-Containern
- Ollama
- ein installiertes Ollama-Modell
- ein Terminal: PowerShell unter Windows oder Terminal unter macOS/Linux

Für diesen Test verwenden wir:

```text
Modell: qwen3.5:9b
Kontextlänge: 64000 Tokens
API-Modus: Chat Completions
```

Die Modellgröße und die benötigte Rechenleistung hängen vom verwendeten Rechner ab. Falls `qwen3.5:9b` zu langsam läuft, kann zunächst ein kleineres Modell verwendet werden.

## 2. Ollama installieren und Modell herunterladen

Ollama kann von der offiziellen Seite installiert werden:

[Ollama herunterladen](https://ollama.com/download)

Nach der Installation prüfen:

```text
ollama --version
```

Das Modell herunterladen:

```text
ollama pull qwen3.5:9b
```

Installierte Modelle anzeigen:

```text
ollama list
```

Der Modellname muss später in Hermes exakt so eingetragen werden, wie er in `ollama list` angezeigt wird.

## 3. Ollama testen

Das Modell direkt testen:

```text
ollama run qwen3.5:9b
```

Zum Beenden des Tests eingeben:

```text
/bye
```

Unter Windows läuft Ollama normalerweise als Hintergrunddienst. Falls Ollama nicht läuft, kann der Dienst manuell gestartet werden:

```text
ollama serve
```

Das Terminal mit `ollama serve` muss dann geöffnet bleiben.

## 4. Hermes-Image und Daten-Volume vorbereiten

```text
docker pull nousresearch/hermes-agent:stable
docker volume create hermes-test-data
```

Optional prüfen:

```text
docker image ls nousresearch/hermes-agent
docker volume inspect hermes-test-data
```

## 5. Ollama in Hermes konfigurieren

Die Hermes-Modellauswahl öffnen:

```powershell
docker run -it --rm `
  -v hermes-test-data:/opt/data `
  nousresearch/hermes-agent:stable model
```

Bei der Anbieterauswahl auswählen:

```text
Custom / OpenAI-compatible endpoint
```

Danach diese Werte eingeben:

```text
API base URL:
http://host.docker.internal:11434/v1
```

```text
API key:
ollama
```

Ollama prüft den API-Schlüssel nicht. Hermes erwartet jedoch möglicherweise einen Eintrag; `ollama` dient hier als Platzhalter.

Bei der Kompatibilität auswählen:

```text
Chat Completions
```

Bei der Modellabfrage eingeben:

```text
qwen3.5:9b
```

Bei der Kontextlänge eingeben:

```text
64000
```

Die Modellfamilie unterstützt ein größeres Kontextfenster. Für Hermes wird zunächst 64.000 verwendet, weil Werkzeugbeschreibungen, Dateien und Gesprächsverlauf viel Kontext benötigen und größere Werte mehr Arbeitsspeicher beziehungsweise VRAM beanspruchen.

Bei der Abfrage zum Anzeigenamen kann eingetragen werden:

```text
Ollama Qwen3.5 9B
```

Bei der Abfrage zum Reasoning-Aufwand für den ersten Test `low` auswählen und mit **Enter** bestätigen.

## 6. Terminal-Backend festlegen

Hermes läuft bereits in Docker. Für den ersten Test wird daher das lokale Terminal-Backend des Hermes-Containers verwendet:

```powershell
docker run -it --rm `
  -v hermes-test-data:/opt/data `
  nousresearch/hermes-agent:stable config set terminal.backend local
```

## 7. Hermes starten

Aus dem Hermes-Projektordner starten:

```powershell
docker run -it --rm `
  -v hermes-test-data:/opt/data `
  --mount "type=bind,source=${PWD},target=/workspace" `
  nousresearch/hermes-agent:stable chat --toolsets "terminal,file"
```

Der Parameter `--mount` stellt den aktuellen Projektordner im Container unter `/workspace` bereit. Dadurch kann Hermes Dateien aus dem Projekt lesen und dort Ergebnisse speichern.

Wenn der Projektordner nicht benötigt wird, reicht:

```powershell
docker run -it --rm `
  -v hermes-test-data:/opt/data `
  nousresearch/hermes-agent:stable chat --toolsets "terminal,file"
```

## 8. Verbindung testen

Im Hermes-Chat eingeben:

```text
Antworte kurz auf Deutsch: Welches Modell wird in dieser Sitzung verwendet?
```

Danach einen Werkzeugtest durchführen:

```text
Lege unter /opt/data/team-tests die Datei hermes-ollama-test.txt mit genau dem Inhalt „Ollama funktioniert“. Lies die Datei anschließend wieder ein und zeige mir den vollständigen Pfad und den Inhalt.
```

## 9. Ergebnis unabhängig prüfen

Hermes mit folgendem Befehl beenden:

```text
/quit
```

Die Datei anschließend direkt aus dem Docker-Volume lesen:

```powershell
docker run --rm `
  -v hermes-test-data:/opt/data `
  nousresearch/hermes-agent:stable `
  bash -lc "cat /opt/data/team-tests/hermes-ollama-test.txt"
```

Erwartete Ausgabe:

```text
Ollama funktioniert
```

## 10. Fehlerbehebung

### Hermes erreicht Ollama nicht

Prüfen, ob Ollama auf dem Windows-Host erreichbar ist:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

Werden die installierten Modelle angezeigt, läuft Ollama. In Hermes muss trotzdem diese Adresse verwendet werden:

```text
http://host.docker.internal:11434/v1
```

`localhost` würde innerhalb des Hermes-Containers auf den Container selbst und nicht auf Windows zeigen.

### Modell nicht gefunden

```powershell
ollama list
```

Den dort angezeigten Namen exakt in Hermes eintragen, zum Beispiel `qwen3.5:9b`.

### Antworten sind sehr langsam oder Ollama beendet sich

- Kontextlänge zunächst auf `32000` oder `64000` begrenzen.
- Ein kleineres Modell verwenden.
- Andere speicherintensive Programme schließen.
- Prüfen, ob ausreichend RAM oder VRAM verfügbar ist.

### Verbindung unter Linux

Bei Linux kann je nach Docker-Konfiguration eine andere Netzwerkadresse erforderlich sein. Wenn Ollama auf dem Host läuft, kann Hermes mit Host-Netzwerk gestartet werden:

```bash
docker run -it --rm \
  --network host \
  -v hermes-test-data:/opt/data \
  nousresearch/hermes-agent:stable chat --toolsets "terminal,file"
```

In diesem Fall wird als API-Basis normalerweise verwendet:

```text
http://127.0.0.1:11434/v1
```

