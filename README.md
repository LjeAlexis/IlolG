# IlolG - Discord Bot for League of Legends

**IlolG** is a Discord bot designed to enhance the gaming experience for League of Legends players by tracking their in-game performance, LP changes, and leaderboard rankings. Built with Python and the Riot API, IlolG provides real-time updates and insights to engage players within your Discord server.

---

## Features

- 🎮 **Live Match Tracking**: Get notified when registered players start a match.
- 📊 **Post-Match Insights**: View detailed stats after a match, including K/D/A, champion played, and match results.
- 🏆 **Leaderboard Management**: Track player rankings, LP, and win/loss ratios with a daily leaderboard.
- 🤝 **Community Engagement**: Foster competition and camaraderie among players in your server.

---

## Commands

### Player Management
- **`!addplayer <gameName#tagLine>`**  
  Add a player to the tracker (e.g., `!addplayer VisDeButte#2121`).

- **`!removeplayer <summonerName>`**  
  Remove a player from the tracker.

- **`!listplayers`**  
  List all registered players.

### Leaderboard
- **`!leaderboard`**  
  Display the current leaderboard, showing ranks, LP, and win/loss stats.

- **`!resetleaderboard`**  
  Reset the leaderboard data (admin use only).

---

## Installation

### Prerequisites
1. **Python 3.8+** installed on your system.
2. A Riot Games developer account to obtain an API key from the [Riot Developer Portal](https://developer.riotgames.com/).
3. A Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications).

---

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LjeAlexis/IlolG.git
   cd IlolG
    ```
2. **Set up a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
````
3. **Install dependecies:**
````bash
pip install .
`````
4. **Create a .env file in the project root with your credentials:**
```` bash
DISCORD_TOKEN=your_discord_bot_token
RIOT_API_KEY=your_riot_api_key
DISCORD_CHANNEL_ID=your_discord_channel_id
````
5. **Run the bot:
````bash
#If installed as a package
lol-discord-bot

#If running locally:
python -m ilolg.bot
````

## Contributing

Feel free to contribute by submitting issues or pull requests to the [GitHub repository](https://github.com/LjeAlexis/IlolG).

## Licence

This project is licensed under the MIT License. See the LICENSE file for details.

