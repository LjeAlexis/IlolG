import discord
from discord.ext import commands
from features.leaderboard import add_player, remove_player, get_leaderboard, load_players, save_players
from ilolg.lol_api import get_player_puuid

# Initialisation du bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.command(name="addplayer")
async def add_player_command(ctx, summoner_name: str, region: str = "EUW"):
    """Commande pour ajouter un joueur au leaderboard."""
    try:
        await ctx.send(f"Recherche du joueur {summoner_name} dans la région {region}...")
        
        # Récupérer le PUUID via l'API Riot
        puuid = get_player_puuid(summoner_name, tagLine=region, region=region)
        if not puuid:
            await ctx.send(f"Impossible de trouver le joueur {summoner_name} dans la région {region}.")
            return

        # Ajouter le joueur au leaderboard
        if add_player(summoner_name, puuid, region):
            await ctx.send(f"Joueur {summoner_name} ajouté avec succès.")
        else:
            await ctx.send(f"Le joueur {summoner_name} est déjà dans la liste.")
    except Exception as e:
        await ctx.send(f"Erreur lors de l'ajout : {e}")

@bot.command(name="removeplayer")
async def remove_player_command(ctx, summoner_name: str):
    """Commande pour supprimer un joueur du leaderboard."""
    try:
        if remove_player(summoner_name):
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

@bot.command(name="updateleaderboard")
async def update_leaderboard_command(ctx):
    """Commande pour forcer une mise à jour des données du leaderboard."""
    try:
        leaderboard = get_leaderboard()
        save_players(leaderboard)
        await ctx.send("Leaderboard mis à jour avec succès.")
    except Exception as e:
        await ctx.send(f"Erreur lors de la mise à jour : {e}")

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
            message += f"- {player['summoner_name']} ({player['region']})\n"

        await ctx.send(message)
    except Exception as e:
        await ctx.send(f"Erreur lors de l'affichage des joueurs : {e}")

# Lancer le bot avec le token depuis l'environnement
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    print("Token Discord non trouvé. Veuillez le définir dans le fichier .env.")
else:
    bot.run(DISCORD_TOKEN)
