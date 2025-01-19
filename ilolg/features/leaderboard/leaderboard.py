import time
import logging
from ilolg.features.leaderboard.rank_model import RankModel
from ilolg.lol_api import get_player_rank_and_lp
from ilolg.features.manage_player.player_manager import PlayerManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LeaderboardManager:
    def __init__(self, player_manager: PlayerManager):
        self.player_manager = player_manager

    def get_leaderboard(self, force_update: bool = False) -> list[dict]:
        """
        Récupère et met à jour les données des joueurs pour générer le leaderboard.

        Args:
            force_update (bool): Si True, force la mise à jour des données même si elles sont récentes.

        Returns:
            list[dict]: Liste des joueurs triée par LP décroissant et rang.
        """
        players = self.player_manager.load_players()
        leaderboard = []

        for player in players:
            self._ensure_region(player)

            previous_lp = player.get("lp", 0)
            previous_rank = player.get("rank", "Unranked")

            # Actualiser les données si nécessaire
            if force_update or self._needs_update(player):
                self._update_player_rank(player, previous_lp, previous_rank)

            leaderboard.append(player)

        leaderboard.sort(key=self._rank_key)
        self.player_manager.save_players(players)  # Sauvegarde les mises à jour
        return leaderboard

    @staticmethod
    def _ensure_region(player: dict):
        """Assure qu'un joueur a une région par défaut."""
        if "region" not in player:
            player["region"] = "EUW"

    @staticmethod
    def _needs_update(player: dict) -> bool:
        """Vérifie si les données d'un joueur doivent être mises à jour."""
        return time.time() - player.get("last_updated", 0) > 86400  # 24 heures

    def _update_player_rank(self, player: dict, previous_lp: int, previous_rank: str):
        """Met à jour les informations de rang et LP d'un joueur."""
        try:
            #TODO: see the .get 
            rank_and_lp = get_player_rank_and_lp(player["puuid"], player["region"])
            player["rank"] = rank_and_lp.get("rank", "Unranked")
            player["lp"] = rank_and_lp.get("lp", 0)
            player["wins"] = rank_and_lp.get("wins", 0)
            player["losses"] = rank_and_lp.get("losses", 0)
            player["last_updated"] = time.time()

            # Calculer les changements de LP et de rang
            player["lp_change"] = player["lp"] - previous_lp
            player["rank_change"] = (
                f"↗️ {player['rank']}" if player["rank"] != previous_rank else "↔️"
            )
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du joueur {player['summoner_name']}: {e}")

    @staticmethod
    def _rank_key(player: dict):
        """Clé de tri pour le leaderboard."""
        rank_split = player["rank"].split()
        tier = rank_split[0] if len(rank_split) > 0 else "IRON"
        division = rank_split[1] if len(rank_split) > 1 else None

        # Gestion des rangs sans division
        if tier in ["MASTER", "GRANDMASTER", "CHALLENGER"]:
            return -RankModel.get_rank_order(tier), 0, -player["lp"]

        return -RankModel.get_rank_order(tier), RankModel.get_division_order(division or "IV"), -player["lp"]
