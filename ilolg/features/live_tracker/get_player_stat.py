from typing import Optional, Dict, Any
from ilolg.lol_api import get_match_ids, get_match_details
from ilolg.features.live_tracker.stats_model import MatchStats
import logging
logger = logging.getLogger(__name__)


QUEUE_ID_TO_NAME = {
    420: "Ranked Solo/Duo",
    440: "Ranked Flex",
    400: "Normal Draft",
    430: "Normal Blind",
    450: "ARAM",
    700: "Clash",
}

def get_last_match_stats(player: Dict[str, Any]) -> Optional[MatchStats]:
    puuid: str = player["puuid"]
    match_ids: Optional[list[str]] = get_match_ids(puuid, count=1)

    if not match_ids:
        return None

    match_id: str = match_ids[0]
    if player.get("last_match_id") == match_id:
        return None

    match_details: Optional[Dict[str, Any]] = get_match_details(match_id)
    if not match_details:
        return None

    info = match_details.get("info", {})
    participants: list[Dict[str, Any]] = info.get("participants", [])
    queue_id: int = info.get("queueId", 0)

    duration_seconds = None
    start_ms = info.get("gameStartTimestamp")
    end_ms = info.get("gameEndTimestamp")
    if isinstance(start_ms, int) and isinstance(end_ms, int) and end_ms > start_ms:
        duration_seconds = (end_ms - start_ms) // 1000
    else:
        duration_seconds = info.get("gameDuration")  
    is_ranked: bool = queue_id in {420, 440}
    queue_name = QUEUE_ID_TO_NAME.get(queue_id)

    for participant in participants:
        if participant["puuid"] == player["puuid"]:
            return MatchStats(
                match_id=match_id,
                champion=participant["championName"],
                kills=participant["kills"],
                deaths=participant["deaths"],
                assists=participant["assists"],
                role=participant.get("individualPosition", "UNKNOWN"),
                game_mode=info.get("gameMode", "UNKNOWN"),
                win=participant["win"],
                damage_dealt=participant.get("totalDamageDealtToChampions", 0),
                vision_score=participant.get("visionScore", 0),
                ranked=is_ranked,
                duration_seconds=duration_seconds, 
                queue_name=queue_name,              
            )
    return None