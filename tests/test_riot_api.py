import pytest
from ilolg.lol_api import get_player_puuid

def test_get_player_puuid():
    puuid = get_player_puuid("NomDuJoueur")
    assert puuid is not None
