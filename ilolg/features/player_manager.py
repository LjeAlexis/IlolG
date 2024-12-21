import json

PLAYERS_FILE = "data/players.json"

def load_players():
    """Charge les joueurs depuis le fichier JSON."""
    try:
        with open(PLAYERS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_players(players):
    """Sauvegarde les joueurs dans le fichier JSON."""
    with open(PLAYERS_FILE, "w") as file:
        json.dump(players, file, indent=4)

def add_player(summoner_name, puuid):
    """
    Ajoute un joueur à la liste des joueurs.

    Args:
        summoner_name (str): Nom de l'invocateur.
        puuid (str): Identifiant unique du joueur.

    Returns:
        bool: True si le joueur a été ajouté, False s'il existait déjà.
    """
    players = load_players()
    if any(player["puuid"] == puuid for player in players):
        return False  # Le joueur existe déjà
    players.append({"summoner_name": summoner_name, "puuid": puuid})
    save_players(players)
    return True

def remove_player(summoner_name):
    """
    Supprime un joueur de la liste des joueurs.

    Args:
        summoner_name (str): Nom de l'invocateur.

    Returns:
        bool: True si le joueur a été supprimé, False s'il n'existait pas.
    """
    players = load_players()
    updated_players = [player for player in players if player["summoner_name"] != summoner_name]
    if len(players) == len(updated_players):
        return False  # Aucun joueur supprimé
    save_players(updated_players)
    return True
