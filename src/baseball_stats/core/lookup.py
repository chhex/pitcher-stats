"""baseball_stats/core/lookup.py"""

from pathlib import Path
from datetime import date, timedelta

import pandas as pd
from pybaseball import chadwick_register

CACHE_PATH = Path.home() / ".cache" / "pitcher_stats" / "player_register.parquet"
CACHE_MAX_AGE_DAYS = 30


def get_player_register() -> pd.DataFrame:
    """Lädt die komplette Spieler-Registry, gecacht für CACHE_MAX_AGE_DAYS."""
    if CACHE_PATH.exists():
        age = date.today() - date.fromtimestamp(CACHE_PATH.stat().st_mtime)
        if age < timedelta(days=CACHE_MAX_AGE_DAYS):
            return pd.read_parquet(CACHE_PATH)

    register = chadwick_register()
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    register.to_parquet(CACHE_PATH)
    return register


def search_pitchers(register: pd.DataFrame, name: str) -> pd.DataFrame:
    """Sucht Pitcher per Teilstring-Match im vollen Namen (case-insensitive)."""
    register = register.dropna(subset=["key_mlbam", "name_first", "name_last"]).copy()
    register["full_name"] = register["name_first"].str.title() + " " + register["name_last"].str.title()
    return register[register["full_name"].str.contains(name, case=False, na=False)]


def get_pitcher_by_id(register: pd.DataFrame, key_mlbam: int) -> pd.Series | None:
    """Holt einen einzelnen Spieler per ID, z.B. um den Namen für die Anzeige aufzulösen."""
    register = register.dropna(subset=["key_mlbam", "name_first", "name_last"]).copy()
    register["full_name"] = register["name_first"].str.title() + " " + register["name_last"].str.title()
    matches = register[register["key_mlbam"] == key_mlbam]
    if matches.empty:
        return None
    return matches.iloc[0]