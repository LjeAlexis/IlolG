import json
import os

class PlayerManager:
    PLAYERS_FILE = "./data/players.json"

    def __init__(self):
        """
        Initialise le gestionnaire de joueurs.
        Vérifie que le fichier JSON des joueurs existe, sinon le crée.
        """
        self.ensure_players_file_exists()

    @staticmethod
    def default_player_structure(summoner_name, puuid, region):
        """
        Renvoie la structure par défaut d'un joueur.

        Args:
            summoner_name (str): Nom de l'invocateur.
            puuid (str): PUUID du joueur.
            region (str): Région du joueur.

        Returns:
            dict: Structure par défaut d'un joueur.
        """
        return {
            "summoner_name": summoner_name,
            "puuid": puuid,
            "region": region,
            "last_match_id": None  # Initialisé à None par défaut
        }

    def ensure_players_file_exists(self):
        """
        Vérifie que le fichier players.json existe, sinon le crée.
        """
        os.makedirs(os.path.dirname(self.PLAYERS_FILE), exist_ok=True)
        if not os.path.isfile(self.PLAYERS_FILE):
            with open(self.PLAYERS_FILE, "w") as file:
                json.dump([], file)  # Initialise avec une liste vide

    def load_players(self):
        """
        Charge les joueurs depuis le fichier JSON.

        Returns:
            list: Liste des joueurs enregistrés.
        """
        with open(self.PLAYERS_FILE, "r") as file:
            return json.load(file)

    def save_players(self, players):
        """
        Sauvegarde les joueurs dans le fichier JSON.

        Args:
            players (list): Liste des joueurs à sauvegarder.
        """
        with open(self.PLAYERS_FILE, "w") as file:
            json.dump(players, file, indent=4)

    def add_player(self, summoner_name, puuid, region="EUW"):
        """
        Ajoute un joueur à la liste des joueurs.

        Args:
            summoner_name (str): Nom de l'invocateur.
            puuid (str): Identifiant unique du joueur.
            region (str): Région du joueur.

        Returns:
            bool: True si le joueur a été ajouté, False s'il existait déjà.
        """
        players = self.load_players()
        if any(player["puuid"] == puuid for player in players):
            return False  # Le joueur existe déjà

        # Ajoute un joueur avec la structure par défaut
        players.append(self.default_player_structure(summoner_name, puuid, region))
        self.save_players(players)
        return True

    def remove_player(self, summoner_name):
        """
        Supprime un joueur de la liste des joueurs.

        Args:
            summoner_name (str): Nom de l'invocateur.

        Returns:
            bool: True si le joueur a été supprimé, False s'il n'existait pas.
        """
        players = self.load_players()
        updated_players = [player for player in players if player["summoner_name"] != summoner_name]

        if len(players) == len(updated_players):
            return False  # Aucun joueur supprimé

        self.save_players(updated_players)
        return True
