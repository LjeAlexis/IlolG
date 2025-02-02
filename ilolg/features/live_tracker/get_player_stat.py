from typing import Optional, Dict, Any
from ilolg.lol_api import get_match_ids, get_match_details
from ilolg.features.live_tracker.stats_model import MatchStats

def get_last_match_stats(player: Dict[str, Any]) -> Optional[MatchStats]:
    """
    Récupère les statistiques du dernier match d'un joueur.

    Args:
        player (Dict[str, Any]): Informations sur le joueur (puuid, summoner_name, region).

    Returns:
        Optional[MatchStats]: Objet MatchStats contenant les statistiques du joueur, ou None si aucune partie trouvée ou déjà publiée.
    """
    puuid: str = player["puuid"]
    match_ids: Optional[list[str]] = get_match_ids(puuid, count=1)

    if not match_ids:
        print(f"Aucun match trouvé pour {player['summoner_name']}")
        return None

    match_id: str = match_ids[0]
    print(f"Dernier match ID pour {player['summoner_name']}: {match_id}")

    if player.get("last_match_id") == match_id:
        print(f"Match déjà publié pour {player['summoner_name']}: {match_id}")
        return None

    match_details: Optional[Dict[str, Any]] = get_match_details(match_id)

    if not match_details:
        print(f"Impossible d'obtenir les détails pour le match {match_id}")
        return None

    participants: list[Dict[str, Any]] = match_details.get("info", {}).get("participants", [])
    queue_id: int = match_details.get("info", {}).get("queueId", 0)

    # Déterminer si la partie est classée (Ranked)
    ranked_queues = {420, 440}  # 420 = Ranked Solo/Duo, 440 = Ranked Flex
    is_ranked: bool = queue_id in ranked_queues

    for participant in participants:
        if participant["puuid"] == player["puuid"]:
            print(f"Statistiques trouvées pour {player['summoner_name']} : {participant}")

            return MatchStats(
                match_id=match_id,
                champion=participant["championName"],
                kills=participant["kills"],
                deaths=participant["deaths"],
                assists=participant["assists"],
                role=participant.get("individualPosition", "UNKNOWN"),
                game_mode=match_details.get("info", {}).get("gameMode", "UNKNOWN"),
                win=participant["win"],
                damage_dealt=participant.get("totalDamageDealtToChampions", 0),
                vision_score=participant.get("visionScore", 0),
                ranked=is_ranked
            )

    print(f"Pas de statistiques pour {player['summoner_name']} dans le match {match_id}")
    return None
