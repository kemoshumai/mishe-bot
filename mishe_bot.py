import discord
from mishe_repl import repl
from config import CHANNEL_ID

CHANNEL_ID = CHANNEL_ID

class MisheBot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = self.get_channel(CHANNEL_ID)
        await channel.send(repl("貴方は今起きました。挨拶をしてください。"))

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id == CHANNEL_ID:
            if message.content == "/exit":
                channel = self.get_channel(CHANNEL_ID)
                await channel.send("うぐっ（サーバー停止）")
                exit()
            async with message.channel.typing():
                print(f'Message from {message.author}: {message.content}')
                channel = self.get_channel(CHANNEL_ID)
                await channel.send(repl(message.content))
