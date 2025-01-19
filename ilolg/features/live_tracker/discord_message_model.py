from pydantic import BaseModel
from typing import Optional
import discord
import logging
import requests

# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_latest_patch_version() -> str:
    """
    Récupère la dernière version de patch depuis l'API Data Dragon.

    Returns:
        str: La dernière version de patch disponible.
    """
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        versions = response.json()
        if versions:
            return versions[0]  # La première version est la plus récente
    except requests.RequestException as e:
        logger.error(f"Erreur lors de la récupération des versions : {e}")
        return "13.24.1"  # Valeur par défaut si l'API échoue


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
    patch_version: str = get_latest_patch_version()

    def get_champion_icon_url(self) -> str:
        """
        Génère l'URL de l'icône du champion.

        Returns:
            str: URL de l'icône du champion.
        """
        base_url = "https://ddragon.leagueoflegends.com/cdn"
        return f"{base_url}/{self.patch_version}/img/champion/{self.champion}.png"

    def create_embed(self) -> discord.Embed:
        """
        Crée un embed Discord basé sur les statistiques du match.

        Returns:
            discord.Embed: Embed Discord contenant les informations du match.
        """
        # Déterminer la couleur en fonction du résultat
        color = discord.Color.green() if self.win else discord.Color.red()

        # Créer l'embed
        embed = discord.Embed(
            title=f"Match Results for {self.summoner_name}",
            color=color
        )
        embed.add_field(name="Game mode", value=self.game_mode, inline=True)
        embed.add_field(name="Champion", value=self.champion, inline=True)
        embed.add_field(name="Role", value=self.role, inline=True)
        embed.add_field(name="Result", value="Victory 🏆" if self.win else "Defeat ❌", inline=True)
        embed.add_field(name="K/D/A", value=f"{self.kills}/{self.deaths}/{self.assists}", inline=True)
        embed.set_thumbnail(url=self.get_champion_icon_url())  # Ajouter l'icône du champion
        embed.set_footer(text="Tracked by IlolG Bot <3")
        return embed

    def log_match(self):
        """
        Log les informations du match pour le suivi.
        """
        result = "Victory 🏆" if self.win else "Defeat ❌"
        logger.info(
            f"[MATCH RESULT] Summoner: {self.summoner_name}, Champion: {self.champion}, "
            f"Game Mode: {self.game_mode}, Role: {self.role}, "
            f"K/D/A: {self.kills}/{self.deaths}/{self.assists}, Result: {result}, Match ID: {self.match_id}"
        )
