from discord import app_commands
from discord.ext import commands
from cinebot import Movie
from dotenv import load_dotenv
import os
import discord


class MovieInfo(discord.Embed):
    """A class that represents a movie information embed.

    This class extends the discord.Embed class and provides an embed with movie information.
    It sets the title, color, thumbnail, release date, and synopsis fields of the embed.

    Args:
        movie_infos: The movie information object.
        *args: Additional arguments to pass to the discord.Embed constructor.
        **kwargs: Additional keyword arguments to pass to the discord.Embed constructor.

    Attributes:
        title: The title of the movie.
        color: The color of the embed.

    Methods:
        get_embed: Get the movie information embed.

    """

    def __init__(self, movie_infos, *args, **kwargs):
        """Initialize the MovieInfo embed.

        Args:
            movie_infos: The movie information object.
            *args: Additional arguments to pass to the discord.Embed constructor.
            **kwargs: Additional keyword arguments to pass to the discord.Embed constructor.

        """
        super().__init__(*args, **kwargs)
        self.title = movie_infos.title
        self.color = discord.Color.from_rgb(69, 44, 129)

        self.set_thumbnail(
            url=f"https://image.tmdb.org/t/p/w500{movie_infos.poster_path}"
        )

        if movie_infos.release_date:
            self.add_field(
                name="Date de sortie", value=f"{movie_infos.release_date}", inline=False
            )
        else:
            self.add_field(
                name="Date de sortie", value="A determiner | Inconnue", inline=False
            )

        len_overview_movie = len(movie_infos.overview)
        if len_overview_movie > 1900:
            self.add_field(
                name="Synopsis", value=f"{movie_infos.overview[:1900]}...", inline=False
            )
        else:
            self.add_field(
                name="Synopsis", value=f"{movie_infos.overview}", inline=False
            )

    def get_embed(self):
        """Get the movie information embed.

        Returns:
            The movie information embed.

        """

        return self


class MovieSelection(discord.ui.Select):
    """A class that represents a movie selection dropdown.

    This class extends the discord.ui.Select class and provides a dropdown menu for selecting a movie.
    It takes a list of movies as input and creates options for each movie in the dropdown.

    Args:
        list_movie: The list of movies to populate the dropdown options.

    Attributes:
        list_movie: The list of movies.

    Methods:
        callback: The callback method that sends a message with movie information when a movie is selected.

    """

    def __init__(self, list_movie):
        """Initialize the MovieSelection dropdown.

        Args:
            list_movie: The list of movies to populate the dropdown options.

        """
        options = [
            discord.SelectOption(label=f"{list_movie[i].title}", value=f"{i}")
            for i in range(len(list_movie))
        ]
        self.list_movie = list_movie

        super().__init__(
            placeholder="Selectionne un film pour des informations",
            max_values=1,
            min_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        """The callback method that sends a message with movie information when a movie is selected.

        Args:
            interaction: The interaction object.

        Returns:
            None

        """
        movie = self.list_movie[int(self.values[0])]
        await interaction.response.send_message(embed=MovieInfo(movie).get_embed())


class SelectView(discord.ui.View):
    """A class that represents a select view.

    This class extends the discord.ui.View class and provides a view with a movie selection dropdown.
    It takes a list of movies as input and adds a MovieSelection item to the view.

    Args:
        timeout: The timeout duration for the view (default is 60 seconds).
        list_movie: The list of movies to populate the dropdown options.

    Methods:
        None

    """

    def __init__(self, *, timeout=60, list_movie):
        """Initialize the SelectView.

        Args:
            timeout: The timeout duration for the view (default is 60 seconds).
            list_movie: The list of movies to populate the dropdown options.

        """
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
        emb = discord.Embed(
            title="Resultats - 10 films les plus populaires",
            color=discord.Color.from_rgb(69, 44, 129),
        )
        for i, res in enumerate(top_10_results):
            emb.add_field(
                name=f"{i+1} - {res.title}",
                value=f"[Poster de : {res.title}](https://image.tmdb.org/t/p/w500{res.poster_path})",
                inline=False,
            )
        await interaction.response.send_message(
            embed=emb, view=SelectView(list_movie=top_10_results)
        )

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
