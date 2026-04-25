# Vorlesung 1 – Einführung in Docker und Kubernetes (11.04.2026)

HTW Berlin  
Datum: 11.04.2026  
Ort: Berlin  
Verfasser: Zouia Alkurdi & Oliver Richter

---

## Thema der 1. Vorlesung

- Was ist Docker?
- Was ist Kubernetes?
- Warum werden diese Technologien genutzt?
- Einrichtung der Entwicklungsumgebung (Docker + Kubernetes)
- Erste Schritte mit Containern und Pods

---

## Einführung: Was ist Docker?

Docker ist eine Plattform, um **Anwendungen in Containern** auszuführen.  
Ein Container ist wie eine kleine, abgeschlossene Box, in der alles liegt, was eine App braucht:
- der Programmcode
- die Abhängigkeiten (z. B. Bibliotheken, Python-Pakete)
- die Laufzeitumgebung

### Vorteile von Docker
- **Unabhängig vom System**: Container laufen auf jedem Rechner gleich.
- **Leichtgewichtig**: Container sind kleiner und schneller als virtuelle Maschinen.
- **Wiederverwendbar**: Ein Image kann von vielen Personen genutzt werden.
- **Einfacher Start**: Ein Container ist mit einem einzigen Befehl startbar.

### Beispiel
```bash
docker run hello-world
```

---

## Einführung: Was ist Kubernetes?

Kubernetes (oft abgekürzt als "K8s") ist ein System, das viele Docker-Container **verwaltet und steuert**.  
Es sorgt dafür, dass Apps zuverlässig laufen, auch wenn einzelne Container ausfallen.

### Wichtige Funktionen
- **Orchestrierung**: Kubernetes startet, überwacht und beendet Container automatisch.
- **Skalierung**: Kubernetes kann mehr Container starten, wenn die Nachfrage steigt.
- **Self-Healing**: Wenn ein Container abstürzt, wird er automatisch ersetzt.
- **Netzwerk**: Container bekommen automatisch eine Verbindung untereinander.

### Wichtige Begriffe
- **Pod**: kleinste Einheit, enthält einen oder mehrere Container.
- **Deployment**: beschreibt, wie viele Pods einer App laufen sollen.
- **Service**: macht eine App im Netzwerk erreichbar.

---

## Warum Docker und Kubernetes zusammen?

Docker ist gut, um **eine einzelne App in einem Container** laufen zu lassen.  
Wenn aber viele Container und Services zusammenarbeiten sollen, braucht man ein System wie Kubernetes.

- **Docker** = Container bauen und starten
- **Kubernetes** = Container im großen Maßstab betreiben

Beispiel:  
Eine AI-App hat eine **API** (Anfragen beantworten) und einen **Worker** (Modelle berechnen).
- Mit Docker packen wir API und Worker in Container.
- Mit Kubernetes stellen wir sicher, dass beide immer laufen und erreichbar sind.

---

## Entwicklungsumgebung einrichten

# 1. Docker Desktop installieren
# Windows (PowerShell, mit winget)
winget install --id Docker.DockerDesktop -e

# Windows (PowerShell, mit Chocolatey)
choco install docker-desktop -y

# macOS (Homebrew)
brew install --cask docker

# Test ob Docker läuft
docker run hello-world

# 2. Docker Image mit Sicht auf Sicherheit und Update erstellen - Caddy (open source web server)
1. Erstelle ein Dockerfile mit folgenden Inhalt
```bash
FROM caddy:2.11.2-alpine

# Install packages and update system
RUN apk update && apk upgrade --no-cache

# allow binding to 80/443 as non-root
RUN apk add --no-cache libcap \
  && setcap 'cap_net_bind_service=+ep' /usr/bin/caddy

# create caddy user if missing (idempotent)
RUN addgroup -S caddy || true \
  && adduser -S -D -H -G caddy caddy || true

# set permissions for caddy user
RUN chown -R caddy:caddy /data /config

# running rootless
USER caddy
```
2. Baue das Image (Hinweis, Terminal muss sich im gleichen Path wie das Dockerfile befinden)
```bash
docker build -t caddy:2.11.2-alpine-rootless .
```
# 3. Kubernetes in Docker Desktop aktivieren
# Einstellungen-Datei bearbeiten (Pfad abhängig vom System)
1. Docker for Desktop öffnen
2. Setting klicken (links oben das Zahnrad)
3. Links anschliessend Kubernetes wählen
4. Enable Kubernetes aktivieren

# 3. Kubernetes CLI (kubectl) installieren
# Windows
choco install kubernetes-cli

# macOS
brew install kubernetes-cli

# 4. Kubernetes-Cluster testen
kubectl cluster-info
kubectl get nodes

# 5. Caddy im Cluster deployen
1. deployment.yml herunterladen
2. Im Terminal folgendes ausführen (Hinweis, Terminal muss sich im gleichen Path wie die deployment.yml befinden)
```bash
kubectl apply -f deployment.yml
```
3. Alle Pods im k8s Cluster anzeigen lassen
```bash
kubectl get po  
```
Soll folgendes liefern
```bash
NAME                          READY   STATUS    RESTARTS   AGE
web-deploy-78f7cc68c7-75tr7   1/1     Running   0          40s
web-deploy-78f7cc68c7-cch76   1/1     Running   0          40s
web-deploy-78f7cc68c7-dssrp   1/1     Running   0          40s
web-deploy-78f7cc68c7-shcsc   1/1     Running   0          40s
```

# 5. Caddy im Cluster modifizieren
1. Erhöhe die Anzahl der Pods im k8s Cluster (setze die Replicas auf 5)
```bash
replicas: 5 
```
```bash
kubectl apply -f deployment.yml
```
Soll folgendes liefern
```bash
NAME                          READY   STATUS    RESTARTS   AGE
web-deploy-7498b94b57-4xgcn   1/1     Running   0          2m15s
web-deploy-7498b94b57-jvwmq   1/1     Running   0          2m15s
web-deploy-7498b94b57-ld5kz   1/1     Running   0          3s
web-deploy-7498b94b57-njk6w   1/1     Running   0          2m15s
web-deploy-7498b94b57-xgf92   1/1     Running   0          2m15s
```
2. Deployment löschen
```bash
kubectl delete -f deployment.yml
```
```bash
kubectl delete -f deployment.yml
```
Soll folgendes liefern
```bash
No resources found in default namespace.
```
---

## Verbindung zur Aufgabe

Diese Vorlesung bildet die technische Grundlage für die Abgabe:

- **Docker**: App in einem Container starten
- **Kubernetes**: Container als Services betreiben
- **Pitch**: Idee und Umsetzung erklären