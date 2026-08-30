from pydantic import BaseModel

class PitcherMatch(BaseModel):
    key_mlbam: int
    full_name: str
    mlb_played_first: int | None = None
    mlb_played_last: int | None = None

class GameInfo(BaseModel):
    game_pk: int
    game_date: str
    opponent: str
    decision: str  # "W" / "L" / "ND"

class PitchStat(BaseModel):
    pitch_name: str
    count: int
    avg_speed: float
    pct: float

class GameSummary(BaseModel):
    game_date: str
    opponent: str
    decision: str
    innings_pitched: str | None
    earned_runs: int | None
    era: float | None
    total_pitches: int
    strikes: int
    balls: int
    strikeouts: int
    pitch_stats: list[PitchStat]