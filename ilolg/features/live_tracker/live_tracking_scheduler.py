from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ilolg.features.live_tracker.get_player_stat import get_last_match_stats
from ilolg.features.manage_player.player_manager import PlayerManager
import discord
import asyncio

player_manager = PlayerManager()

def start_live_tracker_scheduler(bot, channel_id):
    """
    Démarre le scheduler pour surveiller les joueurs et notifier les résultats.

    Args:
        bot (discord.ext.commands.Bot): Instance du bot Discord.
        channel_id (int): ID du canal Discord pour les notifications.
    """
    scheduler = AsyncIOScheduler()

    @scheduler.scheduled_job("interval", minutes=1)
    async def track_live_games():
        players = player_manager.load_players()
        for player in players:
            stats = get_last_match_stats(player)
            if stats:
                channel = bot.get_channel(channel_id)
                if not channel:
                    print(f"Canal Discord introuvable pour ID : {channel_id}")
                    continue

                color = discord.Color.green() if stats.win else discord.Color.red()

                # Créer l'embed
                embed = discord.Embed(
                    title=f"Match Results for {player['summoner_name']}",
                    color=color
                )
                embed.add_field(name="Game mode", value=stats.game_mode, inline=True)
                embed.add_field(name="Champion", value=stats.champion, inline=True)
                embed.add_field(name="Role", value=stats.role, inline=True)
                embed.add_field(name="Result", value="Victory 🏆" if stats.win else "Defeat ❌", inline=True)
                embed.add_field(name="K/D/A", value=f"{stats.kills}/{stats.deaths}/{stats.assists}", inline=True)
                embed.set_footer(text="Tracked by IlolG Bot <3")

                # Envoyer le message dans le canal Discord
                await channel.send(embed=embed)

                player["last_match_id"] = stats.match_id

        player_manager.save_players(players)

    scheduler.start()
    print("Scheduler du live tracker démarré.")
