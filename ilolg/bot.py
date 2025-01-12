import discord
from discord.ext import commands
from features.leaderboard.leaderboard import get_leaderboard
from features.leaderboard.leaderboard_scheduler import *
from ilolg.lol_api import get_player_puuid
from features.manage_player.player_manager import PlayerManager
from features.live_tracker.live_tracking_scheduler import start_live_tracker_scheduler
import os
from dotenv import load_dotenv



player_manager = PlayerManager()

# Charger les variables d'environnement
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", 0))  # ID du canal Discord

if not DISCORD_TOKEN:
    print("Token Discord non trouvé. Veuillez le définir dans le fichier .env.")
    exit()

if DISCORD_CHANNEL_ID == 0:
    print("ID de canal non trouvé. Veuillez le définir dans le fichier .env.")
    exit()

# Initialisation du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send("Salut tout le monde ! Le bot est en ligne et prêt à fonctionner. 🎉")

    # Démarrer le scheduler
    start_leaderboard_scheduler(bot, DISCORD_CHANNEL_ID)
    start_live_tracker_scheduler(bot, DISCORD_CHANNEL_ID) 



@bot.command(name="addplayer")
async def add_player_command(ctx, riot_id: str):
    """Commande pour ajouter un joueur au leaderboard."""
    try:
        # Vérifier le format Riot ID
        if "#" not in riot_id:
            await ctx.send("Le Riot ID doit être au format `gameName#tagLine` (ex: Alez#8201).")
            return

        game_name, tag_line = riot_id.split("#")
        await ctx.send(f"Recherche du joueur {game_name}#{tag_line} dans la région EUW...")

        # Récupérer le PUUID via l'API Riot
        puuid = get_player_puuid(game_name, tag_line, region="EUW")
        if not puuid:
            await ctx.send(f"Impossible de trouver le joueur {game_name}#{tag_line} dans la région EUW.")
            return

        # Ajouter le joueur via player_manager
        if player_manager.add_player(f"{game_name}#{tag_line}", puuid):
            await ctx.send(f"Joueur {game_name}#{tag_line} ajouté avec succès.")
        else:
            await ctx.send(f"Le joueur {game_name}#{tag_line} est déjà dans la liste.")
    except Exception as e:
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
        await ctx.send(f"Erreur lors de la suppression : {e}")


@bot.command(name="leaderboard")
async def leaderboard_command(ctx):
    """Commande pour afficher le leaderboard avec les ranks et les LP."""
    try:
        leaderboard = get_leaderboard()
        if not leaderboard:
            await ctx.send("Le leaderboard est vide pour l'instant.")
            return

        # Génération du message
        message = "\u2b50 **Leaderboard actuel** \u2b50\n"
        for i, player in enumerate(leaderboard, start=1):
            message += (
                f"{i}. {player['summoner_name']} - {player['rank']} "
                f"({player['lp']} LP, {player['wins']}W/{player['losses']}L)\n"
            )

        await ctx.send(message)
    except Exception as e:
        await ctx.send(f"Erreur lors de l'affichage du leaderboard : {e}")


@bot.command(name="resetleaderboard")
async def reset_leaderboard_command(ctx):
    """Commande pour réinitialiser le leaderboard."""
    try:
        save_players([])  # Vide le fichier JSON
        await ctx.send("Leaderboard réinitialisé avec succès.")
    except Exception as e:
        await ctx.send(f"Erreur lors de la réinitialisation : {e}")


@bot.command(name="listplayers")
async def list_players_command(ctx):
    """Commande pour afficher tous les joueurs enregistrés (sans leurs stats)."""
    try:
        players = load_players()
        if not players:
            await ctx.send("Aucun joueur enregistré.")
            return

        message = "**Joueurs enregistrés :**\n"
        for player in players:
            message += f"- {player['summoner_name']}\n"

        await ctx.send(message)
    except Exception as e:
        await ctx.send(f"Erreur lors de l'affichage des joueurs : {e}")


# Lancer le bot
bot.run(DISCORD_TOKEN)
