from pydantic import BaseModel
from typing import Optional
import discord
import logging
import requests
from datetime import timedelta

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_latest_patch_version() -> str:
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        versions = response.json()
        if versions:
            return versions[0]
    except requests.RequestException as e:
        logger.error(f"Erreur lors de la récupération des versions : {e}")
        return "13.24.1"  # fallback

def fmt_duration(seconds: Optional[int]) -> str:
    if not seconds or seconds < 0:
        return "N/A"
    td = timedelta(seconds=int(seconds))
    # mm:ss si < 1h, sinon H:MM:SS
    total_seconds = int(td.total_seconds())
    if total_seconds < 3600:
        m, s = divmod(total_seconds, 60)
        return f"{m:02d}:{s:02d}"
    else:
        h, rem = divmod(total_seconds, 3600)
        m, s = divmod(rem, 60)
        return f"{h}:{m:02d}:{s:02d}"

class DiscordMatchMessage(BaseModel):
    summoner_name: str
    champion: str
    kills: int
    deaths: int
    assists: int
    role: str
    game_mode: str
    win: bool
    match_id: str
    damage_dealt: int
    vision_score: int
    ranked: bool
    # 👇 nouveaux champs (optionnels)
    duration_seconds: Optional[int] = None
    queue_name: Optional[str] = None

    patch_version: str = get_latest_patch_version()

    def get_champion_icon_url(self) -> str:
        base_url = "https://ddragon.leagueoflegends.com/cdn"
        return f"{base_url}/{self.patch_version}/img/champion/{self.champion}.png"

    def create_embed(self) -> discord.Embed:
        color = discord.Color.green() if self.win else discord.Color.red()
        queue_type = "Ranked" if self.ranked else "Normal"
        queue_label = self.queue_name or queue_type

        title = f"{self.champion} — {'Victory 🏆' if self.win else 'Defeat ❌'} ({queue_label})"
        embed = discord.Embed(title=title, color=color)
        embed.set_author(name=self.summoner_name, icon_url=self.get_champion_icon_url())

        embed.add_field(
            name="📋 Match Info",
            value=(
                f"**Mode:** {self.game_mode}\n"
                f"**Role:** {self.role}\n"
                f"**Queue:** {queue_label}\n"
                f"**Duration:** {fmt_duration(self.duration_seconds)}"
            ),
            inline=False
        )

        embed.add_field(
            name="⚔️ Performance",
            value=(
                f"**K/D/A:** {self.kills}/{self.deaths}/{self.assists}\n"
                f"**Damage:** {self.damage_dealt:,}\n"
                f"**Vision:** {self.vision_score}"
            ),
            inline=False
        )

        embed.set_thumbnail(url=self.get_champion_icon_url())
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text="IlolG Bot — Powered by Riot API")
        return embed

    def log_match(self):
        result = "Victory 🏆" if self.win else "Defeat ❌"
        queue_label = self.queue_name or ("Ranked" if self.ranked else "Normal")
        logger.info(
            f"[MATCH RESULT] Summoner: {self.summoner_name}, Champion: {self.champion}, "
            f"Mode: {self.game_mode}, Queue: {queue_label}, Role: {self.role}, "
            f"K/D/A: {self.kills}/{self.deaths}/{self.assists}, Damage: {self.damage_dealt}, "
            f"Vision: {self.vision_score}, Duration: {fmt_duration(self.duration_seconds)}, "
            f"Result: {result}, Match ID: {self.match_id}"
        )
