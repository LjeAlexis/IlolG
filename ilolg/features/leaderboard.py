import json
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

def add_player(summoner_name, puuid):
    """Ajoute un joueur au fichier."""
    players = load_players()
    if any(player["puuid"] == puuid for player in players):
        return False  # Le joueur est déjà dans la liste
    players.append({"summoner_name": summoner_name, "puuid": puuid})
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
        rank_and_lp = get_player_rank_and_lp(player["puuid"])
        leaderboard.append({
            "summoner_name": player["summoner_name"],
            "rank": rank_and_lp.get("rank", "N/A"),
            "lp": rank_and_lp.get("lp", 0)
        })
    leaderboard.sort(key=lambda x: (-x["lp"], x["rank"]))  # Trier par LP desc et rank
    return leaderboard

def generate_leaderboard():
    """Génère un leaderboard fictif pour les tests."""
    players = load_players()
    leaderboard = []
    for player in players:
        rank_and_lp = get_player_rank_and_lp(player["puuid"])
        leaderboard.append({
            "summoner_name": player["summoner_name"],
            "rank": rank_and_lp.get("rank", "Unranked"),
            "lp": rank_and_lp.get("lp", 0)
        })
    return leaderboard

