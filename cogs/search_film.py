from discord import app_commands
from discord.ext import commands
from cinebot import Movie
from dotenv import load_dotenv
import os
import discord

class MovieInfo(discord.Embed):
    def __init__(self, movie_infos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        movie_infos = movie_infos
        self.title = movie_infos.title
        self.color = discord.Color.from_rgb(69, 44, 129)
        
        self.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{movie_infos.poster_path}")

        if movie_infos.release_date:
            self.add_field(name="Date de sortie", value=f"{movie_infos.release_date}", inline=False)
        else:
            self.add_field(name="Date de sortie", value="A determiner | Inconnue", inline=False)

        len_overview_movie = len(movie_infos.overview)
        if len_overview_movie > 1900:
            self.add_field(name="Synopsis", value=f"{movie_infos.overview[:1900]}...", inline=False)
        else:
            self.add_field(name="Synopsis", value=f"{movie_infos.overview}", inline=False)

    def get_embed(self):
        return self

class MovieSelection(discord.ui.Select):
    def __init__(self, list_movie):
        options=[
            discord.SelectOption(label="Film 1", description="Info sur le film 1!", value='0'),
            discord.SelectOption(label="Film 2", description="Info sur le film 2!", value='1'),
            discord.SelectOption(label="Film 3", description="Info sur le film 3!", value='2'),
            discord.SelectOption(label="Film 4", description="Info sur le film 4!", value='3'),
            discord.SelectOption(label="Film 5", description="Info sur le film 5!", value='4'),
            discord.SelectOption(label="Film 6", description="Info sur le film 6!", value='5'),
            discord.SelectOption(label="Film 7", description="Info sur le film 7!", value='6'),
            discord.SelectOption(label="Film 8", description="Info sur le film 8!", value='7'),
            discord.SelectOption(label="Film 9", description="Info sur le film 9!", value='8'),
            discord.SelectOption(label="Film 10", description="Info sur le film 10!", value='9'),
        ]
        
        self.list_movie = list_movie

        super().__init__(placeholder="Numéro du film pour des informations",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
        movie = self.list_movie[int(self.values[0])]
        await interaction.response.send_message(embed=MovieInfo(movie).get_embed())

class SelectView(discord.ui.View):
    def __init__(self, *, timeout=60, list_movie):
        super().__init__(timeout=timeout)
        self.add_item(MovieSelection(list_movie))

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
        emb = discord.Embed(title="Resultats - 10 films les plus populaires", color=discord.Color.from_rgb(69, 44, 129))
        for i, res in enumerate(top_10_results):
            emb.add_field(name=f"{i+1} - {res.title}", value=f"[Poster de : {res.title}](https://image.tmdb.org/t/p/w500{res.poster_path})", inline=False)
        await interaction.response.send_message(embed=emb, view=SelectView(list_movie=top_10_results))
    
    @app_commands.command()
    async def info(self, interaction, nom_du_film: str):
        """Search for movies and display the top 10 results with their posters.

        Args:
            interaction: The interaction object.
            nom_du_film: The name of the movie to search for.

        Returns:
            None

        """
        self.result = self.movie.search(nom_du_film)
        top_movie = list(self.result.results)[0]

        await interaction.response.send_message(embed=MovieInfo(top_movie).get_embed())
        

async def setup(bot):
    await bot.add_cog(SearchMusic(bot))
