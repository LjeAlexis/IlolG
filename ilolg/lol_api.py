import requests
from config import RIOT_API_KEY

BASE_URL = "https://europe.api.riotgames.com"

REGION_MAP = {
    "EUW": "europe",
    "NA": "americas",
    "KR": "asia",
    "EUNE": "europe",
    # Ajoutez d'autres régions si nécessaire
}

def get_player_puuid(gameName, tagLine, region="EUW"):
    """Récupère le PUUID d'un joueur via l'API Riot avec son Riot ID (gameName + tagLine).

    Args:
        gameName (str): Nom du joueur.
        tagLine (str): TagLine du joueur.
        region (str): Région du joueur (par défaut: EUW).

    Returns:
        str: PUUID du joueur ou None en cas d'erreur.
    """
    try:
        region_base_url = f"https://{REGION_MAP.get(region, 'europe')}.api.riotgames.com"
        url = f"{region_base_url}/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("puuid")
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération du PUUID : {e}")
        return None

def get_summoner_id_from_puuid(puuid, region="EUW"):
    """Récupère le summonerId d'un joueur via son PUUID.

    Args:
        puuid (str): PUUID du joueur.
        region (str): Région du joueur (par défaut: EUW).

    Returns:
        str: summonerId du joueur ou None en cas d'erreur.
    """
    try:
        region_specific_base_url = f"https://{region.lower()}1.api.riotgames.com"
        url = f"{region_specific_base_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("id")
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération du summonerId : {e}")
        return None

def get_player_rank_and_lp(summoner_id, region="EUW"):
    """Récupère les rangs et LP d'un joueur via son summonerId.

    Args:
        summoner_id (str): summonerId du joueur.
        region (str): Région du joueur (par défaut: EUW).

    Returns:
        dict: Détails des stats classées (rang, LP, victoires, défaites).
    """
    try:
        region_specific_base_url = f"https://{region.lower()}1.api.riotgames.com"
        url = f"{region_specific_base_url}/lol/league/v4/entries/by-summoner/{summoner_id}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        solo_duo = next((entry for entry in data if entry["queueType"] == "RANKED_SOLO_5x5"), None)
        if solo_duo:
            return {
                "rank": f"{solo_duo['tier']} {solo_duo['rank']}",
                "lp": solo_duo["leaguePoints"],
                "wins": solo_duo["wins"],
                "losses": solo_duo["losses"]
            }
        return {"rank": "Unranked", "lp": 0, "wins": 0, "losses": 0}
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des stats : {e}")
        return {"rank": "N/A", "lp": 0, "wins": 0, "losses": 0}

