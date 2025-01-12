import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Clé API Riot Games
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

# Token du bot Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

#token du serv discord 
DISCORD_SERV_ID= os.getenv("DISCORD_SERV_ID")

#Token du canal Discord
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

#Schedule Interval 
SCHEDULE_INTERVAL = int(os.getenv("SCHEDULE_INTERVAL", 1))  # Défaut à 60 minutes

print(f"RIOT_API_KEY: {RIOT_API_KEY}")
print(f"DISCORD_TOKEN: {DISCORD_TOKEN}")
print(f"DISCORD_CHANNEL_ID: {DISCORD_CHANNEL_ID}")


