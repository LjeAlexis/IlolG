from pydantic import BaseModel
from typing import Optional

class MatchStats(BaseModel):
    match_id: str
    champion: str
    kills: int
    deaths: int
    assists: int
    role: str
    game_mode: str
    win: bool

    def summary(self) -> str:
        """
        Retourne un résumé lisible des statistiques du match.
        """
        result = "Victory 🏆" if self.win else "Defeat ❌"
        return (
            f"Champion: {self.champion}, Role: {self.role}, Game Mode: {self.game_mode}, "
            f"K/D/A: {self.kills}/{self.deaths}/{self.assists}, Result: {result}"
        )
