from dotenv import load_dotenv
from discord.ext import commands
from cinebot import Client
from datetime import timedelta
import os
import discord
import asyncio

load_dotenv()

API_KEY_TMDB = os.getenv("API_KEY_TMDB")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class CineBot(commands.Bot):
    def __init__(self):
        self.EXTENSIONS = ("cogs.search_info.search",)
        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("/"),
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self):
        for extension in self.EXTENSIONS:
            await bot.load_extension(extension)


bot = CineBot()


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="des films")
    )


@bot.tree.command()
@commands.is_owner()
async def sync(interaction):
    await interaction.response.defer()
    synced = await bot.tree.sync()
    msg = await interaction.followup.send(f"Synced {synced} commands")
    await asyncio.sleep(10)
    await msg.delete()

bot.run(DISCORD_TOKEN)
