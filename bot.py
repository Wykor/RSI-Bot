import discord
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
ALERTS_CHANNEL_ID = int(os.getenv('ALERTS_CHANNEL_ID'))

intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged on as', client.user)
    channel = client.get_channel(ALERTS_CHANNEL_ID)
    while True:
        await channel.send('Hello!')
        await asyncio.sleep(60)

client.run(TOKEN)
