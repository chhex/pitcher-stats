# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from baseball_stats.api.routers import pitchers, games

app = FastAPI(title="Pitcher Stats API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://pitcher-stats.vercel.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pitchers.router)
app.include_router(games.router)