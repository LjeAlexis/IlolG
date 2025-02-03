from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ilolg.lol.features.leaderboard.leaderboard import LeaderboardManager
from ilolg.lol.features.leaderboard.discord_leaderboard import DiscordLeaderboard
from config import SCHEDULE_INTERVAL
import discord
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LeaderboardScheduler:
    #TODO: see discord.ext.commands 
    def __init__(self, bot: discord.ext.commands.Bot, channel_id: int, player_manager):
        """
        Initialise la classe pour gérer le scheduler du leaderboard.

        Args:
            bot (discord.ext.commands.Bot): Instance du bot Discord.
            channel_id (int): ID du canal Discord où publier le leaderboard.
            player_manager: Instance de gestion des joueurs.
        """
        logger.info("🚀 Nouvelle instance de LeaderboardScheduler créée !")
        self.bot = bot
        self.channel_id = channel_id
        self.leaderboard_manager = LeaderboardManager(player_manager)
        self.discord_leaderboard = DiscordLeaderboard(bot, channel_id, self.leaderboard_manager)
        self.scheduler = AsyncIOScheduler()

    async def update_and_publish_leaderboard(self):
        logger.info("Mise à jour et publication du leaderboard déclenchée par le scheduler.")
        try:
            await self.discord_leaderboard.publish_leaderboard(force_update=True)
        except Exception as e:
            logger.error(f"Erreur lors de l'actualisation/publication du leaderboard : {e}")


    def start_scheduler(self):
        """
        Démarre le scheduler pour exécuter la mise à jour et publication du leaderboard à intervalle régulier.
        """
        logger.info("Démarrage du scheduler pour le leaderboard avec un intervalle de %s minutes.", SCHEDULE_INTERVAL)

        if self.scheduler.running:
            logger.warning("Le scheduler est déjà en cours d'exécution, arrêt de la procédure de démarrage.")
            return

        self.scheduler.add_job(self.update_and_publish_leaderboard, "interval", minutes=SCHEDULE_INTERVAL, next_run_time=None)

        self.scheduler.start()
        logger.info("Scheduler démarré avec succès.")

