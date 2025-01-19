from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ilolg.features.leaderboard.leaderboard import LeaderboardManager
from ilolg.features.leaderboard.discord_leaderboard import DiscordLeaderboard
from ilolg.config import SCHEDULE_INTERVAL
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
        self.bot = bot
        self.channel_id = channel_id
        self.leaderboard_manager = LeaderboardManager(player_manager)
        self.discord_leaderboard = DiscordLeaderboard(bot, channel_id, self.leaderboard_manager)
        self.scheduler = AsyncIOScheduler()

    async def update_and_publish_leaderboard(self):
        """
        Actualise les données des joueurs et publie le leaderboard sous forme d'embed Discord.
        """
        try:
            await self.discord_leaderboard.publish_leaderboard(force_update=True)
        except Exception as e:
            logger.error(f"Erreur lors de l'actualisation/publication du leaderboard : {e}")

    def start_scheduler(self):
        """
        Démarre le scheduler pour publier automatiquement le leaderboard à intervalles réguliers.
        """
        @self.scheduler.scheduled_job("interval", minutes=SCHEDULE_INTERVAL)
        async def scheduled_task():
            await self.update_and_publish_leaderboard()

        self.scheduler.start()
        logger.info(f"Scheduler du leaderboard démarré avec un intervalle de {SCHEDULE_INTERVAL} minutes.")
