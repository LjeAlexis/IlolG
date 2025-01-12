from ilolg.lol_api import get_match_ids, get_match_details

def get_last_match_stats(player):
    """
    Récupère les statistiques du dernier match d'un joueur.

    Args:
        player (dict): Informations sur le joueur (puuid, summoner_name, region).

    Returns:
        dict: Statistiques du joueur pour le dernier match, ou None si aucune partie trouvée.
    """
    puuid = player["puuid"]
    match_ids = get_match_ids(puuid, count=1)  # Récupère le dernier match

    if not match_ids:
        print(f"Aucun match trouvé pour {player['summoner_name']}")
        return None

    # Obtenir les détails du dernier match
    match_id = match_ids[0]
    match_details = get_match_details(match_id)

    # Extraire les statistiques pour le joueur
    for participant in match_details.get("info", {}).get("participants", []):
        if participant["summonerName"] == player["summoner_name"]:
            return {
                "kills": participant["kills"],
                "deaths": participant["deaths"],
                "assists": participant["assists"],
                "champion": participant["championName"],
                "win": participant["win"],
                "match_id": match_id
            }
    return None
