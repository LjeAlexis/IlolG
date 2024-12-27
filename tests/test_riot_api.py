from lol_api import get_player_puuid, get_summoner_id_from_puuid, get_player_rank_and_lp

def test_player_stats(gameName, tagLine, region="EUW"):
    print(f"Récupération des informations pour {gameName}#{tagLine} dans la région {region}...")

    puuid = get_player_puuid(gameName, tagLine, region)
    if not puuid:
        print(f"Impossible de récupérer le PUUID pour {gameName}#{tagLine}.")
        return

    print(f"PUUID : {puuid}")

    summoner_id = get_summoner_id_from_puuid(puuid, region)
    if not summoner_id:
        print(f"Impossible de récupérer le summonerId pour le PUUID : {puuid}.")
        return

    print(f"SummonerId : {summoner_id}")

    stats = get_player_rank_and_lp(summoner_id)
    if stats["rank"] == "N/A":
        print(f"Impossible de récupérer les statistiques classées pour le summonerId : {summoner_id}.")
    else:
        print("Statistiques classées :")
        print(f" - Rang : {stats['rank']}")
        print(f" - LP : {stats['lp']}")
        print(f" - Victoires : {stats['wins']}")
        print(f" - Défaites : {stats['losses']}")

if __name__ == "__main__":
    test_player_stats("Skiarah", "euw", region="EUW")
