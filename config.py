import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Clé API Riot Games
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

# Token du bot Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


