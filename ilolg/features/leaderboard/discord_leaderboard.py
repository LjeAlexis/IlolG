import discord
import logging
from ilolg.features.leaderboard.leaderboard import LeaderboardManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DiscordLeaderboard:
    #TODO: see discord.ext.commands 
    def __init__(self, bot: discord.ext.commands.Bot, channel_id: int, leaderboard: LeaderboardManager):
        """
        Initialise la classe pour gérer la publication du leaderboard sur Discord.

        Args:
            bot (discord.ext.commands.Bot): Instance du bot Discord.
            channel_id (int): ID du canal Discord où publier le leaderboard.
            leaderboard (Leaderboard): Instance de la classe Leaderboard pour récupérer les données.
        """
        self.bot = bot
        self.channel_id = channel_id
        self.leaderboard = leaderboard

    async def publish_leaderboard(self, force_update: bool = False):
        """
        Récupère le leaderboard et le publie dans le canal Discord.

        Args:
            force_update (bool): Si True, force la mise à jour des données avant la publication.
        """
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            logger.error(f"Erreur : Impossible de trouver le canal Discord avec l'ID {self.channel_id}.")
            return

        try:
            leaderboard_data = self.leaderboard.get_leaderboard(force_update=force_update)

            # Générer le message embed du leaderboard
            if not leaderboard_data:
                embed = self._create_empty_leaderboard_embed()
            else:
                embed = self._create_leaderboard_embed(leaderboard_data)

            await channel.send(embed=embed)
            logger.info(f"Leaderboard publié dans le canal {self.channel_id}.")
        except Exception as e:
            logger.error(f"Erreur lors de la publication du leaderboard : {e}")

    @staticmethod
    def _create_empty_leaderboard_embed() -> discord.Embed:
        """
        Crée un embed Discord pour un leaderboard vide.

        Returns:
            discord.Embed: Embed indiquant que le leaderboard est vide.
        """
        embed = discord.Embed(
            title="📋 Leaderboard actuel",
            description="Le leaderboard est vide pour l'instant.",
            color=discord.Color.dark_gray(),
        )
        embed.set_footer(text="Suivi par IlolG Bot ❤️")
        return embed

    @staticmethod
    def _create_leaderboard_embed(leaderboard_data: list[dict]) -> discord.Embed:
        """
        Crée un embed Discord formaté avec les données du leaderboard.

        Args:
            leaderboard_data (list[dict]): Liste des joueurs et leurs statistiques.

        Returns:
            discord.Embed: Embed contenant le leaderboard formaté.
        """
        embed = discord.Embed(
            title="📋 Leaderboard actuel",
            description="Classement basé sur les rangs et les LP.",
            color=discord.Color.blue(),
        )

        for i, player in enumerate(leaderboard_data, start=1):
            lp_change = player.get("lp_change", 0)
            lp_change_arrow = "⬆️" if lp_change > 0 else "⬇️" if lp_change < 0 else "↔️"

            # Ajouter un champ pour chaque joueur
            embed.add_field(
                name=f"{i}. {player['summoner_name']} ({player['rank']})",
                value=(
                    f"LP : {player['lp']} LP\n"
                    f"Victoire/Défaite : {player['wins']}W/{player['losses']}L\n"
                    f"Changement : {lp_change_arrow} {abs(lp_change)} LP"
                ),
                inline=False,  
            )

        embed.set_footer(text="Tracked by IlolG Bot ❤️")
        return embed
