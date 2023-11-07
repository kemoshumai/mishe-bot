import discord
from mishe_repl import repl
from config import CHANNEL_ID
import json
import datetime
import glob
import os
import re
import math

CHANNEL_ID = CHANNEL_ID

class MisheBot(discord.Client):

    def __init__(self, *args, intents=None):
        self.history = []
        super().__init__(*args, intents=intents)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = self.get_channel(CHANNEL_ID)
        res, self.history = repl("貴方は今起きました。挨拶をしてください。")
        await channel.send(res)

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id == CHANNEL_ID:
            if message.content == "/exit":
                channel = self.get_channel(CHANNEL_ID)
                await channel.send("うぐっ（サーバー停止）")
                exit()
            if message.content == "/reset":
                self.history = []
                return
            if message.content.startswith("/rollup"):
                indexes = re.findall(r'\d+$', message.content)
                if len(indexes) != 0:
                    length = math.floor( int(str(indexes[-1]))/100.0 * len(self.history) )
                    print("rollup:",length)
                    self.history = self.history[length:]
                return
            if message.content.startswith("/restore"):
                indexes = re.findall(r'\d+$', message.content)
                if len(indexes) != 0:
                    index = int(indexes[-1])
                    files = glob.glob('./logs/*')
                    files = sorted(files, key=os.path.getctime, reverse=True)
                    target_log_file = files[index]
                    print("Trying to read a file: "+target_log_file)
                    with open(target_log_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        print(data)
                        self.history = data
                        print("ANDROID MEMORY RESTORED")
                        print(self.history)
                return
            async with message.channel.typing():
                print(f'Message from {message.author}: {message.content}')
                channel = self.get_channel(CHANNEL_ID)
                res, self.history = repl(message.content, self.history)
                await channel.send(res)
                now = datetime.datetime.now()
                with open("./logs/"+str(now).replace(" ","_").replace(":","-")+".json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(self.history, ensure_ascii=False,indent=2))

