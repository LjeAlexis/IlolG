import json
import time
from ilolg.lol_api import get_player_rank_and_lp

PLAYERS_FILE = "data/players.json"

def load_players():
    """Charge les joueurs depuis le fichier."""
    try:
        with open(PLAYERS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_players(players):
    """Sauvegarde les joueurs dans le fichier."""
    with open(PLAYERS_FILE, "w") as file:
        json.dump(players, file, indent=4)

def add_player(summoner_name, puuid, region="EUW"):
    """Ajoute un joueur au fichier."""
    players = load_players()
    if any(player["puuid"] == puuid for player in players):
        return False  # Le joueur est déjà dans la liste
    players.append({
        "summoner_name": summoner_name,
        "puuid": puuid,
        "region": region,
        "last_updated": 0  # Initialise comme non mis à jour
    })
    save_players(players)
    return True

def remove_player(summoner_name):
    """Supprime un joueur du fichier."""
    players = load_players()
    updated_players = [player for player in players if player["summoner_name"] != summoner_name]
    if len(players) == len(updated_players):
        return False  # Aucun joueur supprimé
    save_players(updated_players)
    return True

def get_leaderboard():
    """Récupère le leaderboard avec les ranks et les LP."""
    players = load_players()
    leaderboard = []

    for player in players:
        # Vérifie si les données sont récentes (moins de 24h)
        if time.time() - player.get("last_updated", 0) > 86400:
            rank_and_lp = get_player_rank_and_lp(player["puuid"], player["region"])
            player["rank"] = rank_and_lp.get("rank", "Unranked")
            player["lp"] = rank_and_lp.get("lp", 0)
            player["wins"] = rank_and_lp.get("wins", 0)
            player["losses"] = rank_and_lp.get("losses", 0)
            player["last_updated"] = time.time()  # Met à jour la timestamp
        leaderboard.append(player)

    save_players(players)  # Sauvegarde les mises à jour
    return sorted(
        leaderboard,
        key=lambda x: (-x["lp"], x["rank"])  # Trier par LP desc et rang
    )
