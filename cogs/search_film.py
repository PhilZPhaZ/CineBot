from discord import app_commands
from discord.ext import commands
from cinebot import Movie
from dotenv import load_dotenv
import os
import discord

class SearchMusic(commands.Cog):
    """A class that represents a search music cog.

    This cog provides functionality to search for movies using the TMDB API.
    It includes a method to get the image URL from a movie result and a command to search for movies and display the top 10 results with their posters.

    Args:
        bot: The instance of the bot.

    Attributes:
        bot: The instance of the bot.
        movie: An instance of the Movie class.

    """

    def __init__(self, bot):
        """Initialize the SearchMusic cog.

        Args:
            bot: The instance of the bot.

        """
        self.bot = bot
        load_dotenv()
        API_KEY_TMDB = os.getenv("API_KEY_TMDB")
        self.movie = Movie(API_KEY_TMDB)

    @app_commands.command()
    async def search(self, interaction, nom_du_film: str):
        """Search for movies and display the top 10 results with their posters.

        Args:
            interaction: The interaction object.
            nom_du_film: The name of the movie to search for.

        Returns:
            None

        """
        self.result = self.movie.search(nom_du_film)
        top_10_results = list(self.result.results)[:10]
        emb = discord.Embed(title="Resultats")
        for i, res in enumerate(top_10_results):
            emb.add_field(name=f"{i+1} - {res.title}", value=f"[Poster de : {res.title}](https://image.tmdb.org/t/p/w500{res.poster_path})", inline=False)
        await interaction.response.send_message(embed=emb)

async def setup(bot):
    await bot.add_cog(SearchMusic(bot))
