# Pitcher Stats API

Ein FastAPI-Backend für die Analyse von MLB-Pitcher-Statistiken auf Basis von [Statcast](https://baseballsavant.mlb.com/)-Daten via [pybaseball](https://github.com/jldbc/pybaseball). Ermöglicht Pitcher-Suche, Auflistung von Spielen in einem Zeitraum, detaillierte Pitch-Mix-Auswertung pro Spiel (inkl. ERA/IP/W-L aus der offiziellen MLB-Boxscore) sowie den Vergleich mehrerer Spiele.

## Features

- **Pitcher-Suche** per Namens-Teilstring, basierend auf der Chadwick-Registry (lokal gecacht)
- **Spiele auflisten** für einen Pitcher in einem beliebigen Datumsbereich
- **Pitch-Mix-Analyse pro Spiel**: Anzahl, Durchschnittsgeschwindigkeit und Anteil je Pitch-Typ
- **Boxscore-Anreicherung**: Innings Pitched, Earned Runs, Game-ERA und Win/Loss/No-Decision aus der offiziellen MLB Stats API
- **In-Memory-Caching** für Boxscore-Abfragen (abgeschlossene Spiele ändern sich nicht mehr)
- Automatische interaktive API-Dokumentation via Swagger UI

## Tech Stack

- **FastAPI** — Web-Framework
- **pybaseball** — Statcast-Datenzugriff
- **pandas** — Datenaggregation
- **requests** — MLB Stats API (Boxscore/ERA/W-L)
- **Uvicorn** — ASGI-Server

## Setup (lokal)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Server starten

```bash
uvicorn baseball_stats.api.main:app --reload
```

Anschliessend:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Docker

**Bauen:**
```bash
docker build -t pitcher-stats .
```

**Lokal starten:**
```bash
docker run -p 8000:8000 -e PORT=8000 pitcher-stats
```

Der Container erwartet den Port über die Umgebungsvariable `PORT` (kompatibel mit Plattformen wie [Render](https://render.com), die den Port dynamisch zuweisen).

## API-Endpunkte (Übersicht)

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET` | `/pitchers/search?name=...` | Pitcher-Suche per Namen |
| `GET` | `/pitchers/{pitcher_id}/games?start=...&end=...` | Spiele im Zeitraum auflisten |
| `GET` | `/pitchers/{pitcher_id}/games/{game_pk}?start=...&end=...` | Pitch-Mix + Boxscore-Daten für ein einzelnes Spiel |

Vollständige, interaktive Referenz siehe Swagger UI.

## Projektstruktur

```
src/baseball_stats/
├── cli.py                 # Interaktives CLI-Tool (questionary-basiert)
├── core/
│   ├── legend.py           # Pitch-Type-Legende (Statcast-Codes → Klarnamen)
│   ├── lookup.py            # Pitcher-Registry & Suche
│   ├── games.py             # Spiele-Fetching & Pitch-Mix-Aggregation
│   └── boxscore.py          # MLB Stats API Boxscore-Anreicherung (ERA/IP/W-L), gecacht
└── api/
    ├── main.py               # FastAPI-App
    ├── schemas.py             # Pydantic-Modelle
    └── routers/
        ├── pitchers.py
        └── games.py
```

## Deployment

Getestet für Deployment auf [Render](https://render.com) (Docker-basiert, Free Tier).

## Bekannte Einschränkungen

- Innings-Pitched-Berechnung im CLI-Pfad (ohne Boxscore-Anreicherung) ist eine Näherung basierend auf Statcast-Events, keine exakte offizielle Zahl.
- Der In-Memory-Cache für Boxscore-Daten geht bei Server-Neustart verloren (kein Problem bei geringer Last, ggf. später durch SQLite ersetzen).
- MLB Stats API (`statsapi.mlb.com`) ist inoffiziell/undokumentiert und kann sich jederzeit ändern.