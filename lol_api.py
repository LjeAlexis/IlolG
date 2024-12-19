import requests
from config import RIOT_API_KEY

BASE_URL = "https://euw1.api.riotgames.com"

def get_player_puuid(summoner_name):
    """
    Récupère le PUUID d'un joueur via l'API Riot.
    
    Args:
        summoner_name (str): Nom de l'invocateur.

    Returns:
        str: PUUID du joueur ou None si le joueur est introuvable.
    """
    try:
        url = f"{BASE_URL}/lol/summoner/v4/summoners/by-name/{summoner_name}"
        response = requests.get(url, headers={"X-Riot-Token": RIOT_API_KEY})
        response.raise_for_status()
        summoner_data = response.json()
        return summoner_data.get("puuid")
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération du PUUID : {e}")
        return None

def get_player_stats(puuid):
    """
    Récupère les statistiques classées d'un joueur via l'API Riot.

    Args:
        puuid (str): PUUID du joueur.

    Returns:
        dict: Statistiques du joueur (rank, LP, wins, losses) ou None.
    """
    try:
        # Récupérer l'ID Summoner à partir du PUUID
        url_summoner = f"{BASE_URL}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        response_summoner = requests.get(url_summoner, headers={"X-Riot-Token": RIOT_API_KEY})
        response_summoner.raise_for_status()
        summoner_data = response_summoner.json()
        summoner_id = summoner_data["id"]

        # Récupérer les stats classées
        url_ranked = f"{BASE_URL}/lol/league/v4/entries/by-summoner/{summoner_id}"
        response_ranked = requests.get(url_ranked, headers={"X-Riot-Token": RIOT_API_KEY})
        response_ranked.raise_for_status()
        ranked_data = response_ranked.json()

        # On ne traite que les données classées Solo/Duo
        solo_duo = next((entry for entry in ranked_data if entry["queueType"] == "RANKED_SOLO_5x5"), None)
        if solo_duo:
            return {
                "rank": f"{solo_duo['tier']} {solo_duo['rank']}",
                "leaguePoints": solo_duo["leaguePoints"],
                "wins": solo_duo["wins"],
                "losses": solo_duo["losses"]
            }
        return None
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des statistiques : {e}")
        return None

def get_recent_matches(puuid, count=5):
    """
    Récupère les IDs des matchs récents pour un joueur.

    Args:
        puuid (str): PUUID du joueur.
        count (int): Nombre de matchs à récupérer.

    Returns:
        list: Liste des IDs de matchs ou une liste vide en cas d'erreur.
    """
    try:
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {"start": 0, "count": count}
        response = requests.get(url, headers={"X-Riot-Token": RIOT_API_KEY}, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des matchs récents : {e}")
        return []

def get_match_details(match_id):
    """
    Récupère les détails d'un match donné via l'API Riot.

    Args:
        match_id (str): ID du match.

    Returns:
        dict: Détails pertinents du match ou None en cas d'erreur.
    """
    try:
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
        response = requests.get(url, headers={"X-Riot-Token": RIOT_API_KEY})
        response.raise_for_status()
        match_data = response.json()

        # Exemple de traitement pour un joueur (à adapter selon le contexte)
        participant_data = match_data["info"]["participants"][0]  # Exemple pour le premier joueur
        return {
            "result": "Victoire" if participant_data["win"] else "Défaite",
            "kda": f"{participant_data['kills']}/{participant_data['deaths']}/{participant_data['assists']}",
            "champion": participant_data["championName"]
        }
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des détails du match : {e}")
        return None
