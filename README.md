# Pitcher Stats

A web app for analyzing MLB pitcher statistics: search for a pitcher, list games within a date range, break down the pitch mix per game (including ERA/IP/W-L pulled from the official MLB boxscore), and compare multiple games side by side.

Built on top of the fantastic [pybaseball](https://github.com/jldbc/pybaseball) library, which makes working with [Statcast](https://baseballsavant.mlb.com/) data (pitch type, velocity, spin rate, etc.) in Python genuinely pleasant — without pybaseball, this project would have taken a lot more effort.

## Structure (Monorepo)

```
pitcher-stats/
├── backend/     # FastAPI backend
└── frontend/    # SvelteKit frontend
```

## Backend

A FastAPI service that processes [pybaseball](https://github.com/jldbc/pybaseball) data and exposes it via a REST API.

**Features:**

- Pitcher search by partial name match, based on the Chadwick registry (cached locally)
- List games for a pitcher within any given date range
- Pitch-mix analysis per game: count, average velocity, and share per pitch type
- Boxscore enrichment: innings pitched, earned runs, game ERA, and win/loss/no-decision from the official MLB Stats API
- In-memory caching for boxscore lookups (completed games never change)
- Automatic interactive API documentation via Swagger UI

**Tech stack:** FastAPI · pybaseball · pandas · requests · Uvicorn

### Setup (local)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Start the server

```bash
uvicorn baseball_stats.api.main:app --reload
```

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Docker

```bash
docker build -t pitcher-stats-api ./backend
docker run -p 8000:8000 -e PORT=8000 pitcher-stats-api
```

Or via Docker Compose from the repo root:

```bash
docker compose up --build
```

### Deployment (Backend)

Deployed on [Render](https://render.com) (Docker-based).

### API endpoints (overview)

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/pitchers/search?name=...` | Search for a pitcher by name |
| `GET` | `/pitchers/{pitcher_id}/games?start=...&end=...` | List games within a date range |
| `GET` | `/pitchers/{pitcher_id}/games/{game_pk}?start=...&end=...` | Pitch mix + boxscore data for a single game |

Full, interactive reference available via Swagger UI.

### Deployment

Deployed on [Render](https://render.com) (Docker-based).

## Frontend

A SvelteKit app that talks to the backend API.

**Tech stack:** SvelteKit · TypeScript · TailwindCSS

**Features:**

- Pitcher search with disambiguation when multiple matches are found
- Date-range-based game listing (only enabled once a pitcher is selected)
- Multi-select of games (including select-all/none) for combined viewing
- Pitch-mix table per game with ERA/IP/decision

### Setup (local)

```bash
cd frontend
npm install
```

Create a `.env` file:

```
VITE_API_URL=http://localhost:8000
```

### Start the dev server

```bash
npm run dev
```

Runs on [http://localhost:5173](http://localhost:5173) by default — the backend needs to be running in parallel (CORS is enabled for `localhost:5173` as well as the production Vercel domain).

### Deployment

Deployed on [Vercel](https://vercel.com) via GitHub import (Root Directory: `frontend`).

## Known limitations

- The innings-pitched calculation on the CLI path (without boxscore enrichment) is an approximation based on Statcast events, not an exact official figure.
- The in-memory cache for boxscore data is lost on server restart (not an issue at low load; could be replaced with SQLite later).
- The MLB Stats API (`statsapi.mlb.com`) is unofficial/undocumented and may change at any time.
- Chadwick registry entries for active players are sometimes missing a career-end year (NaN) — handled explicitly in the backend response.

## Acknowledgments

This project wouldn't have been possible without the genuinely excellent work of the [pybaseball](https://github.com/jldbc/pybaseball) maintainers and contributors — thank you. Thanks also to [FastAPI](https://fastapi.tiangolo.com/) for making the backend a joy to build (Swagger UI for free!) and to [Svelte](https://svelte.dev/) for such a clean, low-ceremony approach to building the frontend. And, last but not least, this project definitely wouldn't have come together this quickly without [Claude](https://claude.ai).
