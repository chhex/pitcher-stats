from fastapi import HTTPException
from pybaseball import statcast_pitcher
import pandas as pd

from baseball_stats.core.boxscore import fetch_game_details
from baseball_stats.core.legend import PITCH_LEGEND

def fetch_games_in_range(pitcher_id, start_date, end_date):
    raw = statcast_pitcher(start_date, end_date, pitcher_id)
    if raw.empty:
        return raw, pd.DataFrame()

    games = (
        raw.groupby("game_pk")
        .agg(
            game_date=("game_date", "first"),
            home_team=("home_team", "first"),
            away_team=("away_team", "first"),
        )
        .reset_index()
        .sort_values("game_date")
    )
    return raw, games

    
def summarize_game(game_df: pd.DataFrame, pitcher_id: int) -> dict:
    game_pk = int(game_df["game_pk"].iloc[0])
    try:
        details = fetch_game_details(game_pk, pitcher_id)
    except ValueError:
        raise HTTPException(status_code=409, detail="Game not yet final, try again later")
    
    pitch_summary = game_df.groupby("pitch_type").agg(
        count=("pitch_type", "size"),
        avg_speed=("release_speed", "mean")
    )
    pitch_summary["pct"] = (pitch_summary["count"] / pitch_summary["count"].sum() * 100).round(1)
    pitch_summary["pitch_name"] = pitch_summary.index.map(PITCH_LEGEND)
    pitch_summary = pitch_summary[["pitch_name", "count", "avg_speed", "pct"]]
    pitch_summary = pitch_summary.sort_values("count", ascending=False)
    pitch_summary.index = pitch_summary.pop("pitch_name")
    pitch_summary.index.name = None

    strikes = game_df["type"].isin(["S", "X"]).sum()
    balls = (game_df["type"] == "B").sum()
    strikeouts = game_df[game_df["events"] == "strikeout"].shape[0]

    return {
        "game_date": game_df["game_date"].iloc[0],
        "opponent": f"{game_df['away_team'].iloc[0]} @ {game_df['home_team'].iloc[0]}",
        "total_pitches": len(game_df),
        "strikes": strikes,
        "balls": balls,
        "strikeouts": strikeouts,
        "innings_pitched": details["innings_pitched"],
        "earned_runs": details["earned_runs"],
        "era": details["era"],
        "decision": details["decision"],
        "pitch_summary": pitch_summary,
    }