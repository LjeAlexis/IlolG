from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ilolg.features.leaderboard.leaderboard import get_leaderboard
import discord
from config import SCHEDULE_INTERVAL


SCHEDULE_INTERVAL = int(SCHEDULE_INTERVAL)

async def update_and_publish_leaderboard(bot, channel_id):
    """
    Actualise les données des joueurs et publie le leaderboard.

    Args:
        bot (discord.ext.commands.Bot): Instance du bot Discord.
        channel_id (int): ID du canal Discord où publier le leaderboard.
    """
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Erreur : Impossible de trouver le canal {channel_id}.")
        return

    try:
        leaderboard = get_leaderboard(force_update=True)

        # Génère le message du leaderboard
        if not leaderboard:
            message = "Le leaderboard est vide pour l'instant."
        else:
            message = "\u2b50 **Leaderboard actuel** \u2b50\n"
            for i, player in enumerate(leaderboard, start=1):
                lp_change = player.get('lp_change', 0)
                if lp_change > 0:
                    lp_change_arrow = "⬆️"
                elif lp_change < 0:
                    lp_change_arrow = "⬇️"
                else:
                    lp_change_arrow = "↔️"

                # Générer la ligne du joueur avec la flèche correspondante
                message += (
                    f"{i}. **{player['summoner_name']}** - *{player['rank']}* "
                    f"({player['lp']} LP, {player['wins']}W/{player['losses']}L) {lp_change_arrow} {abs(lp_change)} LP\n"
                )


        await channel.send(message)
        print(f"Leaderboard publié et mis à jour dans le canal {channel_id}")
    except Exception as e:
        print(f"Erreur lors de l'actualisation/publication du leaderboard : {e}")


def start_leaderboard_scheduler(bot, channel_id):
    """
    Démarre le scheduler pour gérer le leaderboard.

    Args:
        bot (discord.ext.commands.Bot): Instance du bot Discord.
        channel_id (int): ID du canal Discord où publier le leaderboard.
    """
    scheduler = AsyncIOScheduler()

    @scheduler.scheduled_job("interval", minutes=SCHEDULE_INTERVAL) 
    async def scheduled_task():
        await update_and_publish_leaderboard(bot, channel_id)

    scheduler.start()
    print("Scheduler du leaderboard démarré.")
