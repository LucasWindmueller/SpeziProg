from fastapi import FastAPI
import csv

app = FastAPI()

def load_metrics():
    values = []

    with open('../data/interest.csv', newline='', encoding='utf-8') as file:
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

@app.get("/health")
def health():
    return {"status": "ok"}