# ilolg/tft/test.py
from ilolg.tft.tft_tracker import TFTTracker

def main():
    # Remplace par ta clé d'API et le puuid du joueur à suivre
    API_KEY = "RGAPI-8e7ea762-58c4-477f-9ad0-dcf560e90bed"
    PUUID = "Gx-iIy1xrkTCVw3LDPxVqlwI1E2ZL7jmeQnb-bAZP03WnnR1d26OXqbNuuwaNvBAYflnrTNUf-oa4w"
    
    tracker = TFTTracker(api_key=API_KEY, region="euw1")
    stats = tracker.calculate_stats(PUUID, nb_matches=10)
    
    print("Statistiques TFT :")
    print(f"Victoire(s) : {stats['wins']}")
    print(f"Défaite(s) : {stats['losses']}")
    print(f"Changement total de LP : {stats['total_lp_change']}")

if __name__ == "__main__":
    main()
