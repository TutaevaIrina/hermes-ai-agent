# Den Ordner in Irinas Repository pushen

Ziel: [TutaevaIrina/hermes-ai-agent](https://github.com/TutaevaIrina/hermes-ai-agent). Bei der Vorbereitung war das Repository öffentlich; der verbundene Benutzer `Yousefaljawzi2` hatte Schreibzugriff. Die lokale Git-Anmeldung auf dem Laptop muss separat funktionieren.

Dieser Ablauf ergänzt den Unterordner `yousef-local-ollama` auf einem eigenen Branch. Die eigentliche Hermes-Software, Docker-Volumes und Modellgewichte werden damit nicht hochgeladen.

## 1. Git prüfen

In PowerShell:

```powershell
git --version
```

Falls Git nicht gefunden wird, [Git für Windows](https://git-scm.com/downloads/win) installieren und PowerShell neu öffnen.

## 2. Eine neue Arbeitskopie des Team-Repositories anlegen

Der folgende Ordnername ist für eine frische Arbeitskopie vorgesehen. Wenn der Ordner bereits existiert, zuerst den Zustand dort prüfen, statt ihn zu überschreiben oder einfach weitere Befehle auszuführen.

```powershell
Set-Location $env:USERPROFILE
git clone https://github.com/TutaevaIrina/hermes-ai-agent.git hermes-ai-agent-team
Set-Location .\hermes-ai-agent-team
git switch -c yousef/ollama-dashboard
```

Bei einer Fehlermeldung den nächsten Schritt erst ausführen, nachdem sie geklärt wurde. Den Branch-Namen nach einem bereits erfolgten Push wiederverwenden; für eine neue Änderung bewusst einen neuen Namen wählen.

## 3. Das heruntergeladene ZIP in die Arbeitskopie entpacken

Der folgende Befehl setzt voraus, dass das ZIP unter diesem Namen im Downloads-Ordner liegt. Bei einem anderen Download-Ort den Pfad anpassen.

```powershell
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\Hermes_GitHub_Teamordner_2026-10-25.zip" -DestinationPath .
Get-ChildItem -Force .\yousef-local-ollama
```

Es sollen sechs Dateien im Unterordner liegen: `.gitignore`, `README.md`, `config.beispiel.yaml`, `VERSUCHE.md`, `TESTPROMPTS.md` und `GITHUB-PUSH.md`.

## 4. Änderungen gezielt vormerken und prüfen

```powershell
git add -- yousef-local-ollama
git diff --cached --stat
git diff --cached
```

In einer frisch geklonten Arbeitskopie sollen nur die sechs neuen Dateien dieses Ordners vorgemerkt sein. Persönliche `.env`-Dateien, Passwörter, API-Schlüssel, Hermes-Rohdaten, Modelle und vollständige Laufexporte gehören nicht in diesen Commit.

Die `.gitignore` im neuen Unterordner schützt dort angelegte persönliche Dateien. Sie ersetzt nicht die `.gitignore` des gesamten Repositories und wirkt nicht rückwirkend auf bereits getrackte Dateien.

## 5. Commit und Push

```powershell
git commit -m "Dokumentiere lokalen Hermes-Betrieb mit Ollama und Dashboard"
git push -u origin yousef/ollama-dashboard
```

Bei einer Browseranmeldung das eigene GitHub-Konto verwenden. Das verbundene Konto in dieser Zusammenarbeit war `Yousefaljawzi2`. Wenn Git eine fehlende Commit-Identität meldet, den Namen und die gewünschte Commit-E-Mail lokal für dieses Repository konfigurieren; die eigene GitHub-noreply-Adresse steht in GitHub unter Settings → Emails. Keine erfundene E-Mail eintragen.

Ein `403` bzw. Permission-denied-Fehler kann auf eine andere lokale Git-Anmeldung oder fehlenden Schreibzugriff hinweisen. Dann Anmeldung und Repository-Berechtigung prüfen. Bei Konflikten oder einem abgelehnten Push keinen Force-Push verwenden; zuerst die genaue Meldung prüfen.

## 6. Pull Request öffnen

Nach erfolgreichem Push das Repository im Browser öffnen. Über **Compare & pull request** den Branch `yousef/ollama-dashboard` mit `main` vergleichen und einen Pull Request anlegen.

Vorschlag für den Titel:

```text
Lokalen Hermes-Betrieb mit Ollama und Dashboard dokumentieren
```

Vorschlag für die Beschreibung:

```text
Ergänzt die Windows-Anleitung für Hermes im Docker-Container mit lokalem Ollama und dem eingebauten Web-Dashboard.

Der neue Unterordner enthält eine Konfigurationsvorlage, Testprompts, die bisherigen Beobachtungen und den Git-Ablauf. Der Teamzugriff über Tailscale ist als noch offen markiert.

Prüfung: Dateiinhalte, YAML-Vorlage, Git-Ignore-Regeln und ZIP-Inhalt wurden geprüft. Ein vollständiger neuer Windows-Installationslauf wurde nicht durchgeführt.
```

Der Push legt den Branch im Team-Repository ab. Die Übernahme nach `main` erfolgt anschließend über den Pull Request.

## Quellen

- [GitHub: Dateien zum Repository hinzufügen](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)
- [GitHub: Commits pushen](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository)
- [GitHub: Anmeldung über Git Credential Manager](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git)
