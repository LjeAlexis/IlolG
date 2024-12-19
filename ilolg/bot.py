from features.leaderboard import add_player, remove_player, get_leaderboard
from ilolg.lol_api import get_player_puuid

@bot.command(name="addplayer")
async def add_player_command(ctx, summoner_name: str):
    """Commande pour ajouter un joueur au leaderboard."""
    try:
        # Récupérer le PUUID via l'API Riot
        puuid = get_player_puuid(summoner_name)
        if not puuid:
            await ctx.send(f"Impossible de trouver le joueur : {summoner_name}.")
            return

        if add_player(summoner_name, puuid):
            await ctx.send(f"Joueur {summoner_name} ajouté avec succès.")
        else:
            await ctx.send(f"Le joueur {summoner_name} est déjà dans la liste.")
    except Exception as e:
        await ctx.send(f"Erreur lors de l'ajout : {e}")

@bot.command(name="removeplayer")
async def remove_player_command(ctx, summoner_name: str):
    """Commande pour supprimer un joueur du leaderboard."""
    if remove_player(summoner_name):
        await ctx.send(f"Joueur {summoner_name} supprimé avec succès.")
    else:
        await ctx.send(f"Le joueur {summoner_name} n'existe pas dans la liste.")

@bot.command(name="leaderboard")
async def leaderboard_command(ctx):
    """Commande pour afficher le leaderboard avec les ranks et les LP."""
    try:
        leaderboard = get_leaderboard()
        if not leaderboard:
            await ctx.send("Le leaderboard est vide pour l'instant.")
            return

        message = "\u2b50 **Leaderboard actuel** \u2b50\n"
        for i, player in enumerate(leaderboard, start=1):
            message += f"{i}. {player['summoner_name']} - {player['rank']} ({player['lp']} LP)\n"

        await ctx.send(message)
    except Exception as e:
        await ctx.send(f"Erreur lors de l'affichage du leaderboard : {e}")
