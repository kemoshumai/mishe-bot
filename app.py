import discord
from mishe_bot import MisheBot
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = MisheBot(intents=intents)

client.run(DISCORD_TOKEN)