from fastapi import FastAPI
from baseball_stats.api.routers import pitchers, games

app = FastAPI(title="Pitcher Stats API")
app.include_router(pitchers.router)
app.include_router(games.router)