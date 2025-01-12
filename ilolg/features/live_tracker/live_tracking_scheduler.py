from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ilolg.features.live_tracker.live_tracking import get_last_match_stats
from ilolg.features.manage_player.player_manager import load_players
import asyncio

def start_live_tracker_scheduler(bot, channel_id):
    """
    Démarre le scheduler pour surveiller les joueurs et notifier les résultats.

    Args:
        bot (discord.ext.commands.Bot): Instance du bot Discord.
        channel_id (int): ID du canal Discord pour les notifications.
    """
    scheduler = AsyncIOScheduler()

    @scheduler.scheduled_job("interval", minutes=10)
    async def track_live_games():
        players = load_players()
        for player in players:
            stats = get_last_match_stats(player)
            if stats:
                channel = bot.get_channel(channel_id)
                if not channel:
                    continue

                result = "victoire" if stats["win"] else "défaite"
                await channel.send(
                    f"**{player['summoner_name']}** a terminé une partie avec :\n"
                    f"- Champion : {stats['champion']}\n"
                    f"- Résultat : {result}\n"
                    f"- K/D/A : {stats['kills']}/{stats['deaths']}/{stats['assists']}\n"
                    f"- Match ID : {stats['match_id']}"
                )

    scheduler.start()
    print("Scheduler du live tracker démarré.")
