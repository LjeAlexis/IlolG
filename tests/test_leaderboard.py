import pytest
from ilolg.features.leaderboard import generate_leaderboard, format_leaderboard
from ilolg.features.player_manager import load_players, save_players

@pytest.fixture
def mock_players():
    """Fixture pour simuler une liste de joueurs."""
    return [
        {"summoner_name": "Player1", "puuid": "puuid1"},
        {"summoner_name": "Player2", "puuid": "puuid2"},
    ]

@pytest.fixture
def mock_leaderboard_data():
    """Fixture pour simuler des données de leaderboard."""
    return [
        {"summoner_name": "Player1", "rank": "Gold IV", "lp": 50, "wins": 10, "losses": 5},
        {"summoner_name": "Player2", "rank": "Silver I", "lp": 75, "wins": 12, "losses": 8},
    ]

def test_generate_leaderboard(mocker, mock_players, mock_leaderboard_data):
    """Test de la génération du leaderboard."""
    mocker.patch("lol_discord_bot.features.leaderboard.load_players", return_value=mock_players)
    mocker.patch("lol_discord_bot.features.leaderboard.get_player_stats", side_effect=lambda puuid: {
        "puuid1": mock_leaderboard_data[0],
        "puuid2": mock_leaderboard_data[1]
    }.get(puuid, None))

    leaderboard = generate_leaderboard()
    assert len(leaderboard) == len(mock_players)
    assert leaderboard[0]["summoner_name"] == "Player1"

def test_format_leaderboard(mock_leaderboard_data):
    """Test de la mise en forme du leaderboard."""
    formatted = format_leaderboard(mock_leaderboard_data)
    assert "Player1" in formatted
    assert "Gold IV" in formatted
    assert "50 LP" in formatted
    assert "Player2" in formatted

def test_save_and_load_players(mock_players, tmp_path):
    """Test du chargement et de la sauvegarde des joueurs."""
    test_file = tmp_path / "players.json"
    save_players(mock_players)
    loaded_players = load_players()
    assert len(loaded_players) == len(mock_players)
    assert loaded_players[0]["summoner_name"] == "Player1"
