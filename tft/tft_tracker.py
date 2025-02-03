import requests

class TFTTracker:
    def __init__(self, api_key: str, region: str = "euw1"):
        self.api_key = api_key
        self.region = region
        # Exemple d'URL de base, à adapter selon la documentation
        self.base_url = f"https://{region}.api.riotgames.com/tft/"

    def get_match_ids(self, puuid: str, start: int = 0, count: int = 20) -> list:
        """
        Récupère une liste d'identifiants de matchs pour un joueur (via son PUUID).
        """
        url = f"{self.base_url}match/v1/matches/by-puuid/{puuid}/ids"
        params = {"api_key": self.api_key, "start": start, "count": count}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_match_details(self, match_id: str) -> dict:
        """
        Récupère les détails d'un match donné.
        """
        url = f"{self.base_url}match/v1/matches/{match_id}"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def analyze_match(self, match_details: dict, puuid: str) -> dict:
        """
        Analyse les détails d'un match pour en extraire :
          - victoire/défaite
          - changement de LP (gain ou perte)
        La structure exacte dépend de la réponse de l’API.
        """
        # Exemple d'analyse (à adapter selon la structure renvoyée par l'API)
        result = {
            "win": False,
            "lp_change": 0
        }
        
        # Supposons que l'API renvoie une liste de participants dans "info" > "participants"
        for participant in match_details.get("info", {}).get("participants", []):
            if participant.get("puuid") == puuid:
                # On suppose que le booléen "placement" indique la victoire (par exemple, placement 1 = victoire)
                result["win"] = (participant.get("placement") == 1)
                # Et que "lp_change" est fourni
                result["lp_change"] = participant.get("lp_change", 0)
                break
        return result

    def calculate_stats(self, puuid: str, nb_matches: int = 20) -> dict:
        """
        Récupère et analyse les nb_matches les plus récentes pour calculer :
          - le nombre de victoires et de défaites
          - le total des gains/pertes de LP
        """
        match_ids = self.get_match_ids(puuid, count=nb_matches)
        wins = 0
        losses = 0
        total_lp_change = 0

        for match_id in match_ids:
            details = self.get_match_details(match_id)
            match_result = self.analyze_match(details, puuid)
            if match_result["win"]:
                wins += 1
            else:
                losses += 1
            total_lp_change += match_result["lp_change"]

        return {
            "wins": wins,
            "losses": losses,
            "total_lp_change": total_lp_change,
            "nb_matches": nb_matches
        }
