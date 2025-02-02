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
    damage_dealt: int
    vision_score: int
    ranked: bool

    def summary(self) -> str:
        """
        Retourne un résumé lisible des statistiques du match.
        """
        result = "Victory 🏆" if self.win else "Defeat ❌"
        ranked_status = "Ranked 🏆" if self.ranked else "Normal ⚔️"
        return (
            f"Champion: {self.champion}, Role: {self.role}, {ranked_status}, Game Mode: {self.game_mode}, "
            f"K/D/A: {self.kills}/{self.deaths}/{self.assists}, "
            f"Damage Dealt: {self.damage_dealt}, Vision Score: {self.vision_score}, "
            f"Result: {result}"
        )
