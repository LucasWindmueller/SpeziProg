### Aufgabe 3 – Data Service (API)

Die CSV-Dateien sind bereits im Ordner `data` gespeichert.
Die Kennzahlen sind bereits berechnet.

**Kopiert den bisherigen Projektstand in einen neuen Ordner und benennt diesen in `3. Aufgabe` um.**

---

### Schritt 1 – Python Umgebung (wichtig)

Erstellt eine virtuelle Umgebung:

```bash
python3 -m venv venv
source venv/bin/activate
```

Installiert anschließend die benötigten Pakete:

```bash
pip3 install fastapi uvicorn
```

### Schritt 2 – main.py anpassen

Ersetzt euren bisherigen Code durch folgenden Code:

```python
from fastapi import FastAPI
import csv

app = FastAPI()

def load_metrics():
    values = []

    with open('../data/Interest.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if not row:
                continue

            if row[0] == "Time":
                continue

            value = row[1]

            if value == "<1":
                value = 0

            if value == "":
                continue

            values.append(int(value))

    mean = sum(values) / len(values)
    peak = max(values)

    first = values[0]
    last = values[-1]

    if last > first:
        trend = "increasing"
    elif last < first:
        trend = "decreasing"
    else:
        trend = "stable"

    return {
        "terms": [
            {
                "name": "coffee",
                "mean": round(mean, 1),
                "peak": peak,
                "trend": trend
            }
        ]
    }

@app.get("/metrics")
def get_metrics():
    return load_metrics()
```

### Schritt 3 – Service starten

Startet den Service mit:
```bash
python -m uvicorn main:app --reload
```

### Schritt 4 – API testen

Öffnet im Browser:
```bash
http://127.0.0.1:8000/metrics
```

### Beispiel erwartetes Ergebnis
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