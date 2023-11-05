from dotenv import load_dotenv
from discord.ext import commands
import os
import discord

load_dotenv()

API_KEY_TMDB = os.getenv("API_KEY_TMDB")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class CineBot(commands.Bot):
    def __init__(self):
        self.EXTENSIONS = ("cogs.search_film",)
        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('/'), intents=intents, help_command=None)

    async def setup_hook(self):
        for extension in self.EXTENSIONS:
            await bot.load_extension(extension)

bot = CineBot()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="des films"))

    await bot.tree.sync()

bot.run(DISCORD_TOKEN)
        