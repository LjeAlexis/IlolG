from ilolg.features.live_tracker.stats_model import MatchStats


def test_match_stats():
    stats = MatchStats(
        match_id="EUW1_123456789",
        champion="Ahri",
        kills=5,
        deaths=3,
        assists=7,
        role="MIDDLE",
        game_mode="CLASSIC",
        win=True
    )

    print("Affichage brut :")
    print(stats.model_dump())
    print("\nAffichage JSON :")
    print(stats.model_dump_json(indent=4))
    print("\nRésumé :")
    print(stats)

test_match_stats()
