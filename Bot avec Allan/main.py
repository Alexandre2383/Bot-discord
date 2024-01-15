
import discord
from discord.ext import commands
from decouple import config

DISCORD_TOKEN=config('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.author != self.user and message.content == "1":
            channel = self.get_channel(message.channel.id)
            await channel.send("https://media.giphy.com/media/LVdLjTsJAWZbu1dzmk/giphy.gif")
            await channel.send("2")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)
client = MyClient(intents=intents)

client.run(DISCORD_TOKEN)