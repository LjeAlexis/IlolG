import requests
import json
from urllib.parse import quote
from ilolg.config import RIOT_API_KEY

# --- mapping régions
REGION_MAP = {
    "EUW": "europe",
    "EUNE": "europe",
    "NA": "americas",
    "KR": "asia",
}

def _continent_base(region: str) -> str:
    return f"https://{REGION_MAP.get(region, 'europe')}.api.riotgames.com"

def _platform_base(region: str) -> str:
    # EUW -> euw1, NA -> na1, KR -> kr1
    return f"https://{region.lower()}1.api.riotgames.com"

def get_player_puuid(gameName, tagLine, region="EUW"):
    try:
        url = f"{_continent_base(region)}/riot/account/v1/accounts/by-riot-id/{quote(gameName)}/{quote(tagLine)}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 429:
            raise RuntimeError("Riot API rate limit (429). Réessaie dans quelques secondes.")
        resp.raise_for_status()
        data = resp.json()
        puuid = data.get("puuid")
        if not puuid:
            raise RuntimeError(f"PUUID introuvable pour {gameName}#{tagLine} (réponse: {data})")
        return puuid
    except requests.HTTPError as e:
        raise RuntimeError(f"Riot API error {e.response.status_code}: {e.response.text[:200]}") from e
    except json.JSONDecodeError:
        raise RuntimeError(f"Réponse non-JSON de Riot : {resp.text[:200]}")
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur réseau Riot API: {e}") from e

def get_summoner_id_from_puuid(puuid, region="EUW"):
    try:
        url = f"{_platform_base(region)}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 429:
            raise RuntimeError("Riot API rate limit (429) sur summoner.")
        resp.raise_for_status()
        return resp.json().get("id")
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur lors de la récupération du summonerId : {e}") from e

def get_player_rank_and_lp(puuid, region="EUW"):
    try:
        summoner_id = get_summoner_id_from_puuid(puuid, region=region)
        if not summoner_id:
            return {"rank": "Unranked", "lp": 0, "wins": 0, "losses": 0}
        url = f"{_platform_base(region)}/lol/league/v4/entries/by-summoner/{summoner_id}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 429:
            return {"rank": "RateLimited", "lp": 0, "wins": 0, "losses": 0}
        resp.raise_for_status()
        entries = resp.json()
        solo = next((e for e in entries if e.get("queueType") == "RANKED_SOLO_5x5"), None)
        if solo:
            return {
                "rank": f"{solo.get('tier','')} {solo.get('rank','')}".strip() or "Unranked",
                "lp": solo.get("leaguePoints", 0),
                "wins": solo.get("wins", 0),
                "losses": solo.get("losses", 0),
            }
        return {"rank": "Unranked", "lp": 0, "wins": 0, "losses": 0}
    except requests.RequestException:
        return {"rank": "N/A", "lp": 0, "wins": 0, "losses": 0}

def get_match_ids(puuid, start=0, count=1, region="EUW"):
    try:
        url = f"{_continent_base(region)}/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 429:
            # renvoie une liste vide pour éviter le spam ; ton scheduler réessaiera plus tard
            return []
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des IDs des matchs : {e}")
        return []

def get_match_details(match_id, region="EUW"):
    try:
        url = f"{_continent_base(region)}/lol/match/v5/matches/{match_id}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 429:
            return {}
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des détails du match : {e}")
        return {}
