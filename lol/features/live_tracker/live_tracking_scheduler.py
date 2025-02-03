from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lol.features.live_tracker.get_player_stat import get_last_match_stats
from lol.features.manage_player.player_manager import PlayerManager
from lol.features.live_tracker.discord_message_model import DiscordMatchMessage
from discord.ext.commands import Bot

import logging

# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

player_manager = PlayerManager()

def start_live_tracker_scheduler(bot: Bot, channel_id: int):
    """
    Démarre le scheduler pour surveiller les joueurs et notifier les résultats.

    Args:
        bot (discord.ext.commands.Bot): Instance du bot Discord.
        channel_id (int): ID du canal Discord pour les notifications.
    """
    scheduler = AsyncIOScheduler()

    @scheduler.scheduled_job("interval", minutes=1)
    async def track_live_games():
        """
        Récupère les statistiques des joueurs et publie les résultats sur Discord.
        """
        players = player_manager.load_players()
        logger.info(f"{len(players)} joueurs chargés pour le suivi.")

        for player in players:
            try:
                stats = get_last_match_stats(player)
                if stats:
                    # Créer un objet DiscordMatchMessage
                    message = DiscordMatchMessage(
                        summoner_name=player["summoner_name"],
                        champion=stats.champion,
                        kills=stats.kills,
                        deaths=stats.deaths,
                        assists=stats.assists,
                        role=stats.role,
                        game_mode=stats.game_mode,
                        win=stats.win,
                        match_id=stats.match_id,
                        damage_dealt=stats.damage_dealt,
                        vision_score=stats.vision_score,
                        ranked=stats.ranked
                    )

                    # Log du match
                    message.log_match()

                    # Envoyer le message sur Discord
                    channel = bot.get_channel(channel_id)
                    if channel:
                        embed = message.create_embed()
                        await channel.send(embed=embed)
                        logger.info(f"Message envoyé pour le joueur {player['summoner_name']}.")
                    else:
                        logger.error(f"Canal introuvable pour l'ID {channel_id}.")

                    # Mettre à jour le dernier match publié
                    player["last_match_id"] = stats.match_id
                else:
                    logger.info(f"Aucun nouveau match trouvé pour {player['summoner_name']}.")
            except Exception as e:
                logger.error(f"Erreur lors du suivi pour {player['summoner_name']}: {e}")

        # Sauvegarder les mises à jour des joueurs
        player_manager.save_players(players)
        logger.info("Mises à jour des joueurs sauvegardées.")

    scheduler.start()
    logger.info("Scheduler du live tracker démarré.")
