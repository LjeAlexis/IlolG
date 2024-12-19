import json

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
