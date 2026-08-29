from fastapi import APIRouter, HTTPException
from baseball_stats.api.schemas import GameInfo, GameSummary, PitchStat
from baseball_stats.core.games import fetch_games_in_range, summarize_game

router = APIRouter(prefix="/pitchers/{pitcher_id}/games", tags=["games"])

@router.get("", response_model=list[GameInfo])
def list_games(pitcher_id: int, start: str, end: str):
    print(f"Fetching games for pitcher_id={pitcher_id} from {start} to {end}")
    raw, games = fetch_games_in_range(pitcher_id, start, end)
    if games.empty:
        return []
    return [
        GameInfo(
            game_pk=int(row.game_pk),
            game_date=row.game_date,
            opponent=f"{row.away_team} @ {row.home_team}",
        )
        for row in games.itertuples()
    ]


@router.get("/{game_pk}", response_model=GameSummary)
def game_summary(pitcher_id: int, game_pk: int, start: str, end: str):
    # TODO: raw-Daten idealerweise cachen statt bei jedem Call neu zu holen
    raw, _ = fetch_games_in_range(pitcher_id, start, end)
    game_df = raw[raw["game_pk"] == game_pk]
    if game_df.empty:
        raise HTTPException(status_code=404, detail="Game not found in given range")

    summary = summarize_game(game_df, pitcher_id)
    return GameSummary(
        game_date=summary["game_date"],
        opponent=summary["opponent"],
        decision=summary["decision"],
        innings_pitched=summary["innings_pitched"],
        earned_runs=summary["earned_runs"],
        era=summary["era"],
        total_pitches=summary["total_pitches"],
        strikes=summary["strikes"],
        balls=summary["balls"],
        strikeouts=summary["strikeouts"],
        pitch_stats=[
            PitchStat(pitch_name=name, count=r["count"], avg_speed=r["avg_speed"], pct=r["pct"])
            for name, r in summary["pitch_summary"].iterrows()
        ],
  )