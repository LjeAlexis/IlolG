import json
from utils.rank_model import RankModel  
import time
from ilolg.lol_api import get_player_rank_and_lp

PLAYERS_FILE = "./ilolg/data/players.json"

def load_players():
    """Charge les joueurs depuis le fichier."""
    try:
        print(f"Chargement du fichier : {PLAYERS_FILE}")
        with open(PLAYERS_FILE, "r") as file:
            players = json.load(file)
            print(f"Joueurs chargés : {players}")
            return players
    except FileNotFoundError:
        print(f"Fichier {PLAYERS_FILE} introuvable. Retourne une liste vide.")
        return []
    except json.JSONDecodeError:
        print(f"Fichier {PLAYERS_FILE} vide ou corrompu. Réinitialisation avec une liste vide.")
        save_players([])  
        return []

def save_players(players):
    """Sauvegarde les joueurs dans le fichier."""
    try:
        print(f"Sauvegarde des joueurs : {players}")
        with open(PLAYERS_FILE, "w") as file:
            json.dump(players, file, indent=4)
        print("Sauvegarde réussie.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")
        raise


def get_leaderboard(force_update=False):
    """
    Récupère le leaderboard avec les ranks et les LP.

    Args:
        force_update (bool): Si True, force la mise à jour des données même si elles sont récentes.

    Returns:
        list: Liste des joueurs triée par LP décroissant et rang.
    """
    players = load_players()
    leaderboard = []

    for player in players:
        previous_lp = player.get("lp", 0)
        previous_rank = player.get("rank", "Unranked")

        # Forcer l'actualisation ou vérifier si les données sont récentes
        if force_update or time.time() - player.get("last_updated", 0) > 0:  # Toujours mettre à jour
            rank_and_lp = get_player_rank_and_lp(player["puuid"], player["region"])
            player["rank"] = rank_and_lp.get("rank", "Unranked")
            player["lp"] = rank_and_lp.get("lp", 0)
            player["wins"] = rank_and_lp.get("wins", 0)
            player["losses"] = rank_and_lp.get("losses", 0)
            player["last_updated"] = time.time()  # Met à jour la timestamp

            # Calculer les changements de LP et de rangs
            player["lp_change"] = player["lp"] - previous_lp
            player["rank_change"] = (
                f"↗️ {player['rank']}" if player["rank"] != previous_rank else "↔️"
            )

        leaderboard.append(player)

def rank_key(player):
    rank_split = player["rank"].split()  # Ex: "SILVER II" -> ["SILVER", "II"]
    tier = rank_split[0] if len(rank_split) > 0 else "IRON"
    division = rank_split[1] if len(rank_split) > 1 else None

    # Gestion des rangs sans division (MASTER, GRANDMASTER, CHALLENGER)
    if tier in ["MASTER", "GRANDMASTER", "CHALLENGER"]:
        return (
            -RankModel.get_rank_order(tier),  
            0,  
            -player["lp"]  
        )

    return (
        -RankModel.get_rank_order(tier),  
        RankModel.get_division_order(division if division else "IV"),  
        -player["lp"]  
    )
