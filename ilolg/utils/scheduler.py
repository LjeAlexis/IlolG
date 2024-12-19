from apscheduler.schedulers.asyncio import AsyncIOScheduler
from features.leaderboard import generate_leaderboard, format_leaderboard

def start_scheduler(bot):
    scheduler = AsyncIOScheduler()

    @scheduler.scheduled_job("cron", hour=9)  # Publier tous les jours à 9h
    async def post_leaderboard():
        channel_id = 123456789  # ID du salon Discord
        channel = bot.get_channel(channel_id)

        if channel:
            leaderboard = generate_leaderboard()
            formatted = format_leaderboard(leaderboard)
            await channel.send(formatted)

    scheduler.start()
