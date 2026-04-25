## Aufgabe 5 – Health Endpoint und Docker Compose

Nachdem der Data Service im Docker-Container läuft, wird der Service nun um einen zusätzlichen Endpoint erweitert und anschließend mit Docker Compose gestartet.

Ziel:
- zusätzlichen Endpoint `/health` erstellen
- Anwendung mit Docker Compose starten
- Service strukturiert und reproduzierbar ausführen

**Kopiert den bisherigen Projektstand in einen neuen Ordner und benennt diesen in `5. Aufgabe` um.**

---

### Schritt 1 – Health Endpoint hinzufügen

Erweitert eure Datei `main.py` um einen zusätzlichen Endpoint:

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

Die Datei enthält damit jetzt mindestens zwei Endpoints:
- `GET /metrics`
- `GET /health`

### Schritt 2 – Health Endpoint testen

Startet den Service lokal und prüft im Browser:
```bash
http://127.0.0.1:8000/health
```

### Beispiel erwartetes Ergebnis
```json
{
  "status": "ok"
}
```

### Schritt 3 – docker-compose.yml erstellen
Erstellt im Projekt-Root eine Datei mit dem Namen docker-compose.yml.

Inhalt:
```yaml
services:
  data-service:
    build:
      context: .
      dockerfile: data-service/Dockerfile
    ports:
      - "8000:8000"
```

Falls der Service noch lokal oder per `docker run` läuft, beendet diesen vorher.

### Schritt 4 – Anwendung mit Docker Compose starten
Startet den Service im Projekt-Root mit:
```bash
docker compose up --build -d
```

### Schritt 5 – API testen
Prüft im Browser beide Endpoints:
```bash
http://localhost:8000/metrics
http://localhost:8000/health
```

### Beispiel erwartete Ergebnisse
/metrics
```json
{
  "terms": [
    {
      "name": "coffee",
      "mean": 72.9,
      "peak": 100,
      "trend": "decreasing"
    }
  ]
}
```
/health
```json
{
  "status": "ok"
}
```

Wenn beide Endpoints erreichbar sind, läuft euer Data Service erfolgreich über Docker Compose.

Zum Beenden:
```bash
docker compose down
```