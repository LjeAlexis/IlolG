import discord
from discord.ext import commands
from ilolg.lol.features.leaderboard.leaderboard_scheduler import LeaderboardScheduler
from ilolg.lol.features.leaderboard.discord_leaderboard import DiscordLeaderboard
from ilolg.lol.features.manage_player.player_manager import PlayerManager
from ilolg.lol.lol_api import get_player_puuid
from ilolg.lol.features.live_tracker.live_tracking_scheduler import start_live_tracker_scheduler
from dotenv import load_dotenv
import os
import logging
import sys
import uuid

#TODO: Message explicite dans un premier temps, ensuite gérer les log de manière centralisé
# Configuration globale des logs
logging.basicConfig(
    level=logging.DEBUG,  # Changez à INFO si vous ne voulez pas trop de détails
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  
    ]
)

logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", 0))  # ID du canal Discord

# Initialisation du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialisation des gestionnaires
player_manager = PlayerManager()
leaderboard_scheduler = LeaderboardScheduler(bot, DISCORD_CHANNEL_ID, player_manager)
discord_leaderboard = DiscordLeaderboard(bot, DISCORD_CHANNEL_ID, leaderboard_scheduler.leaderboard_manager)

@bot.event
async def on_ready():
    logger.info("Bot connecté en tant que %s", bot.user)
    channel = bot.get_channel(DISCORD_CHANNEL_ID)

    if channel:
        await channel.send("Salut tout le monde ! Le bot est en ligne et prêt à fonctionner. 🎉")

    # Démarrer les schedulers
    leaderboard_scheduler.start_scheduler()
    start_live_tracker_scheduler(bot, DISCORD_CHANNEL_ID)

@bot.command(name="addplayer")
async def add_player_command(ctx, riot_id: str):
    """Commande pour ajouter un joueur au leaderboard."""
    try:
        if "#" not in riot_id:
            await ctx.send("Le Riot ID doit être au format `gameName#tagLine` (ex: Alez#8201).")
            return

        game_name, tag_line = riot_id.split("#")
        await ctx.send(f"Recherche du joueur {game_name}#{tag_line} dans la région EUW...")

        puuid = get_player_puuid(game_name, tag_line, region="EUW")
        if not puuid:
            await ctx.send(f"Impossible de trouver le joueur {game_name}#{tag_line} dans la région EUW.")
            return

        if player_manager.add_player(f"{game_name}#{tag_line}", puuid):
            await ctx.send(f"Joueur {game_name}#{tag_line} ajouté avec succès.")
        else:
            await ctx.send(f"Le joueur {game_name}#{tag_line} est déjà dans la liste.")
    except Exception as e:
        logger.error("Erreur lors de l'ajout d'un joueur : %s", e)
        await ctx.send(f"Erreur lors de l'ajout : {e}")

@bot.command(name="removeplayer")
async def remove_player_command(ctx, summoner_name: str):
    """Commande pour supprimer un joueur du leaderboard."""
    try:
        if player_manager.remove_player(summoner_name):
            await ctx.send(f"Joueur {summoner_name} supprimé avec succès.")
        else:
            await ctx.send(f"Le joueur {summoner_name} n'existe pas dans la liste.")
    except Exception as e:
        logger.error("Erreur lors de la suppression d'un joueur : %s", e)
        await ctx.send(f"Erreur lors de la suppression : {e}")

@bot.command(name="leaderboard")
async def leaderboard_command(ctx):
    request_id = uuid.uuid4()  # Génère un identifiant unique
    logger.info(f"[{request_id}] Commande !leaderboard exécutée par {ctx.author} dans {ctx.channel}, publication en cours.")
    try:
        await discord_leaderboard.publish_leaderboard(force_update=False)
    except Exception as e:
        logger.error(f"[{request_id}] Erreur lors de l'exécution de !leaderboard : {e}")
        await ctx.send(f"Erreur : {e}")


@bot.command(name="listplayers")
async def list_players_command(ctx):
    """Commande pour afficher tous les joueurs enregistrés."""
    try:
        players = player_manager.load_players()
        if not players:
            await ctx.send("Aucun joueur enregistré.")
            return

        embed = discord.Embed(
            title="Liste des joueurs enregistrés",
            color=discord.Color.green(),
        )
        for player in players:
            embed.add_field(name=player["summoner_name"], value="\u200b", inline=False)

        await ctx.send(embed=embed)
    except Exception as e:
        logger.error("Erreur lors de l'affichage des joueurs : %s", e)
        await ctx.send(f"Erreur lors de l'affichage des joueurs : {e}")


def main():
    if not DISCORD_TOKEN:
        logger.error("Erreur : DISCORD_TOKEN non trouvé.")
        return
    if DISCORD_CHANNEL_ID == 0:
        logger.error("Erreur : DISCORD_CHANNEL_ID non trouvé.")
        return

    logger.info("Démarrage du bot...")
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
