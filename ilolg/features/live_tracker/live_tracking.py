from ilolg.lol_api import get_match_ids, get_match_details

def get_last_match_stats(player):
    """
    Récupère les statistiques du dernier match d'un joueur.

    Args:
        player (dict): Informations sur le joueur (puuid, summoner_name, region).

    Returns:
        dict: Statistiques du joueur pour le dernier match, ou None si aucune partie trouvée ou déjà publiée.
    """
    puuid = player["puuid"]
    match_ids = get_match_ids(puuid, count=1)  # Récupère le dernier match

    if not match_ids:
        print(f"Aucun match trouvé pour {player['summoner_name']}")
        return None

    # Obtenir l'ID du dernier match
    match_id = match_ids[0]
    print(f"Dernier match ID pour {player['summoner_name']}: {match_id}")

    # Vérifier si le match a déjà été publié
    if player.get("last_match_id") == match_id:
        print(f"Match déjà publié pour {player['summoner_name']}: {match_id}")
        return None

    # Obtenir les détails du dernier match
    match_details = get_match_details(match_id)

    if not match_details:
        print(f"Impossible d'obtenir les détails pour le match {match_id}")
        return None

    # Extraire les participants depuis les détails du match
    participants = match_details.get("info", {}).get("participants", [])
    for participant in participants:
        if participant["puuid"] == player["puuid"]:
            print(f"Statistiques trouvées pour {player['summoner_name']}: {participant}")
            return {
                "kills": participant["kills"],
                "deaths": participant["deaths"],
                "assists": participant["assists"],
                "champion": participant["championName"],
                "win": participant["win"],
                "match_id": match_id
            }

    print(f"Pas de statistiques pour {player['summoner_name']} dans le match {match_id}")
    return None
