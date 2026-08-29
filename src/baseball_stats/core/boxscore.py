import requests
from functools import lru_cache

@lru_cache(maxsize=2048)
def fetch_game_details(game_pk: int, pitcher_id: int) -> dict:
    url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
    data = requests.get(url, timeout=10).json()
    live = data.get("liveData", {})

    is_final = data.get("gameData", {}).get("status", {}).get("abstractGameState") == "Final"
    if not is_final:
        # Nicht cachen — Exception statt Rückgabewert, damit lru_cache nichts speichert
        raise ValueError(f"Game {game_pk} is not final yet")

    decisions = live.get("decisions", {})
    if decisions.get("winner", {}).get("id") == pitcher_id:
        decision = "W"
    elif decisions.get("loser", {}).get("id") == pitcher_id:
        decision = "L"
    else:
        decision = "ND"

    boxscore_teams = live.get("boxscore", {}).get("teams", {})
    pitching_stats = None
    for side in ("home", "away"):
        players = boxscore_teams.get(side, {}).get("players", {})
        player = players.get(f"ID{pitcher_id}")
        if player:
            pitching_stats = player.get("stats", {}).get("pitching", {})
            break

    if not pitching_stats:
        return {"decision": decision, "innings_pitched": None, "earned_runs": None, "era": None}

    ip_str = pitching_stats.get("inningsPitched", "0.0")
    earned_runs = pitching_stats.get("earnedRuns", 0)
    whole, _, partial_outs = ip_str.partition(".")
    ip_decimal = int(whole) + int(partial_outs or 0) / 3
    game_era = (earned_runs * 9 / ip_decimal) if ip_decimal > 0 else 0.0

    return {
        "decision": decision,
        "innings_pitched": ip_str,
        "earned_runs": earned_runs,
        "era": round(game_era, 2),
    }