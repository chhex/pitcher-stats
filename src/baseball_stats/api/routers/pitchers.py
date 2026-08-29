from fastapi import APIRouter
from baseball_stats.core.lookup import get_player_register, search_pitchers
from baseball_stats.api.schemas import PitcherMatch

router = APIRouter(prefix="/pitchers", tags=["pitchers"])

@router.get("/search", response_model=list[PitcherMatch])
def search(name: str):
    register = get_player_register()
    matches = search_pitchers(register, name)
    return [
        PitcherMatch(
            key_mlbam=row.key_mlbam,
            full_name=row.full_name,
            mlb_played_first=row.mlb_played_first,
            mlb_played_last=row.mlb_played_last,
        )
        for row in matches.itertuples()
    ]