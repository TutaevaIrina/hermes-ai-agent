# Hermes lokal mit Ollama und Web-Dashboard

Ergänzung zum Team-Repository [TutaevaIrina/hermes-ai-agent](https://github.com/TutaevaIrina/hermes-ai-agent). Die Haupt-README beschreibt den Groq-Einstieg; dieser Unterordner dokumentiert den lokalen Windows-Aufbau mit Ollama. Dokumentationsstand: 25.10.2026.

## Was hier geteilt wird

Dieser Ordner enthält die Anleitung, eine Konfigurationsvorlage und die bisherigen Beobachtungen. Die Hermes-Oberfläche stammt aus dem offiziellen Hermes-Image von Nous Research. GitHub speichert die Projektdateien; der Chat benötigt weiterhin einen laufenden Hermes-Dienst und einen erreichbaren Modellserver.

| Bestandteil | In der beobachteten Einrichtung |
| --- | --- |
| Oberfläche | Hermes-Web-Dashboard im Browser, `http://127.0.0.1:9119` |
| Agent | Docker-Container `hermes-web`, Image `nousresearch/hermes-agent:stable` |
| Modellserver | Ollama auf dem Windows-Host |
| Hauptmodell | `hermes-projekt:latest`, Anbieter `custom` |
| Modelladresse im Container | `http://host.docker.internal:11434/v1` |
| Persönliche Daten | Docker-Volume `hermes-local-data`, im Container `/opt/data` |

Die Base URL wurde mit `hermes config get model.base_url` ausgelesen. Der Modellname wurde im Dashboard angezeigt. Ein einfacher Chat-Test antwortete korrekt mit „Verbindung funktioniert.“.

Der Name eines Ollama-Modells allein garantiert auf verschiedenen Rechnern keine gleichen Modellgewichte oder Parameter. Vor einem Teamvergleich Modellherkunft, Digest, Kontext und Einstellungen abgleichen. Der ursprüngliche Basis-Modellname des lokalen Alias wird hier nicht nachträglich behauptet.

## Vorhandene Installation prüfen

Diese PowerShell-Befehle lesen den aktuellen Zustand:

```powershell
docker ps --filter "volume=hermes-local-data" --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Image}}"
docker exec hermes-web hermes config get model.base_url
docker exec hermes-web hermes config get model.default
docker exec hermes-web hermes config get agent.max_turns
ollama list
```

Die gewünschte Durchlaufgrenze für die nächsten Versuche ist `agent.max_turns: 8`. Im Dashboard wurde das Feld auf 8 gestellt; der gespeicherte Wert ist mit dem obigen Befehl zu prüfen. `goals.max_turns` ist eine eigene Einstellung.

## Einrichtung auf einem weiteren Windows-Rechner

Voraussetzungen: laufendes Docker Desktop mit Linux-Containern, Ollama auf Windows und das im Team vereinbarte Modell. Jedes Teammitglied hat eigene lokale Volumes und Zugangsdaten. Ein gleicher Volume-Name synchronisiert keine Dateien zwischen Rechnern.

1. Vorhandene Hermes-Container mit demselben Datenvolume beenden, bevor ein neuer Container dieses Volume verwendet.
2. Das Volume bei einer neuen Einrichtung anlegen und den Modellassistenten öffnen:

```powershell
docker volume create hermes-local-data
docker run -it --rm -v hermes-local-data:/opt/data nousresearch/hermes-agent:stable model
```

Im Modellassistenten den benutzerdefinierten OpenAI-kompatiblen Zugang wählen:

| Feld | Einstellung |
| --- | --- |
| Base URL | `http://host.docker.internal:11434/v1` |
| API-Modus | Chat Completions |
| Modell | der tatsächlich in `ollama list` vorhandene, vereinbarte Modellname |
| API-Schlüssel | für die hier beobachtete lokale Ollama-Installation leer |
| Reasoning | für die Bedingung ohne Reasoning `none` |

3. Terminal-Backend und Durchlaufgrenze im selben Volume konfigurieren, solange noch kein Dashboard-Container läuft:

```powershell
docker run --rm -v hermes-local-data:/opt/data nousresearch/hermes-agent:stable config set terminal.backend local
docker run --rm -v hermes-local-data:/opt/data nousresearch/hermes-agent:stable config set agent.max_turns 8
```

4. Ein persönliches Dashboard-Passwort erzeugen und den Container starten. Den folgenden Block nur für eine neue Einrichtung ausführen; ein bestehender Container namens `hermes-web` wird dadurch nicht ersetzt.

```powershell
$env:HERMES_DASHBOARD_BASIC_AUTH_PASSWORD = [guid]::NewGuid().ToString("N")
$env:HERMES_DASHBOARD_BASIC_AUTH_SECRET = [guid]::NewGuid().ToString("N") + [guid]::NewGuid().ToString("N")
Write-Host "Dein Dashboard-Passwort: $env:HERMES_DASHBOARD_BASIC_AUTH_PASSWORD"
docker run -d --name hermes-web --restart unless-stopped -v hermes-local-data:/opt/data -p 127.0.0.1:9119:9119 -e HERMES_DASHBOARD=1 -e HERMES_DASHBOARD_HOST=0.0.0.0 -e HERMES_DASHBOARD_BASIC_AUTH_USERNAME=team -e HERMES_DASHBOARD_BASIC_AUTH_PASSWORD -e HERMES_DASHBOARD_BASIC_AUTH_SECRET nousresearch/hermes-agent:stable gateway run
```

5. Im Browser `http://127.0.0.1:9119` öffnen. Bei dieser neuen Einrichtung mit Benutzername `team` und dem gerade erzeugten Passwort anmelden. Yousefs bereits bestehende Einrichtung verwendet den Benutzernamen `yousef`.
6. Unter **Modelle / Main model** den Modellnamen prüfen. Die Base URL mit dem oben genannten Lesebefehl prüfen.
7. Im Chat den Verbindungstest aus `TESTPROMPTS.md` durchführen.

Das Passwort und der Signierschlüssel werden erst auf dem eigenen Rechner erzeugt. Diese Anleitung enthält keine echten Zugangsdaten.

## Werkzeuge und Vergleichsbedingungen

Für die frühe Web-Recherche wurde DuckDuckGo (`ddgs`) konfiguriert. Dieser Anbieter liefert Suche; der beobachtete Abrufversuch mit `web_extract` scheiterte am Search-only-Backend. Dateien lassen sich bei Bedarf über das Terminal herunterladen.

Vor jeder Vergleichsreihe Modell, Reasoning, Kontext, Toolsets, Skills und die Durchlaufgrenze protokollieren. Ein zuletzt gezeigter Dashboard-Banner listete 21 Werkzeuge und 53 Skills. Frühere CLI-Aufrufe verwendeten explizite Toolset-Parameter. Der Wechsel zur Oberfläche übernimmt diese Aufrufparameter nicht automatisch als gleiche Versuchsbedingungen.

Im Chat jede Zeile einzeln eingeben:

```text
/new
/reasoning none
```

Für die andere Reasoning-Bedingung nach einem neuen Gespräch `/reasoning medium` verwenden. Die Befehle und ihren bestätigten Zustand protokollieren.

## Beobachteter Startkonflikt

Zwei Container verwendeten gleichzeitig `hermes-local-data`. Der neue Gateway brach wiederholt mit folgender Meldung ab:

```text
Cannot reserve gateway profiles: Gateway runtime already owns profile /opt/data
```

Der bisherige Container wurde gestoppt und `hermes-web` neu gestartet. Anschließend gelang der Chat-Test. Container-Namen sind auf jedem Rechner vor einem Stop-Befehl anhand der Containerliste zu prüfen.

Diagnose am vorhandenen Container:

```powershell
docker logs --tail 80 hermes-web
docker exec hermes-web /command/s6-svdt -n 8 /run/service/gateway-default
docker exec hermes-web tail -n 40 /opt/data/logs/errors.log
```

## Versionen und bisherige Ergebnisse

Die beobachtete Hermes-Version war `v0.22.5 (2026.9.24)`, upstream `bf0203a7`. `stable` ist ein veränderlicher Image-Tag. Für Vergleichsläufe den tatsächlichen Digest festhalten:

```powershell
docker image inspect nousresearch/hermes-agent:stable --format '{{index .RepoDigests 0}}'
ollama show --modelfile hermes-projekt:latest
```

Ergebnisse und Grenzen stehen in `VERSUCHE.md`. Das ist eine Zusammenfassung der hier gezeigten Protokolle, keine Sammlung neu ausgeführter Tests.

## Zugang für das Team

Das Dashboard ist derzeit an den lokalen Hostport gebunden. Der Repository-Zugriff allein stellt keine Verbindung zum Dashboard her. Für den geplanten Zugriff von anderen Orten ist Tailscale vorgesehen; Installation und funktionierender Teamzugriff sind bisher nicht bestätigt. Solange der Dienst auf dem Laptop läuft, müssen Laptop, Docker und Ollama verfügbar bleiben.

## Prüfumfang dieses Ordners

Die ursprünglichen manuellen Docker-Befehle und die genannten Ergebnisse stammen aus den bereitgestellten Ausgaben. Die Anleitung für einen weiteren Rechner und der neue Git-Ablauf wurden vorbereitet und statisch geprüft. Ein vollständiger neuer Windows-Installationslauf und ein Git-Push vom Laptop wurden hier nicht ausgeführt.

## Quellen

- [Hermes in Docker](https://hermes-agent.nousresearch.com/docs/user-guide/docker)
- [Hermes-Web-Dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard)
- [Hermes-Modellkonfiguration](https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models)
- [Ollama: OpenAI-Kompatibilität](https://docs.ollama.com/api/openai-compatibility)
- [Dateien zu GitHub hinzufügen](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)
