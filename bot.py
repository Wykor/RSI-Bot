
import discord
import os
import asyncio
import logging

from discord.ext import commands
from dotenv import load_dotenv
from db_helpers import add_alert_channel
from models import AlertChannel
from db_setup import Session

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
session = Session()

@bot.event
async def on_ready():
    logger.info('Logged on as', bot.user.name)
    while True:
        for channel_obj in session.query(AlertChannel).all():
            channel = bot.get_channel(int(channel_obj.channel_id))
            await channel.send('This is an alert!')
        await asyncio.sleep(60)

@bot.command(name='setup_alerts')
async def setup_alerts(ctx):
    channel = ctx.channel

    success = add_alert_channel(session, channel.id)
    if success:
        await ctx.send(f'Alerts setup for {channel.name}!')
    else:
        await ctx.send(f'Alerts already setup for {channel.name}!')

bot.run(TOKEN)
