import contextlib
from discord import app_commands
from discord.ext import commands
from cinebot import InfoSearch, Client
from dotenv import load_dotenv
import os
import discord


# --------------------------- Movie ------------------------------
class MovieInfo(discord.Embed):
    """
    A class that represents a movie information embed.

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
        """
        Initialize the MovieInfo embed.

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
                name="Date de sortie", value=f"{movie_infos.release_date}", inline=True
            )
        else:
            self.add_field(
                name="Date de sortie", value="A determiner | Inconnue", inline=True
            )

        self.add_field(
            name="Réalisateur", value=movie_infos.director, inline=True
        )
        self.add_field(
            name="Note moyenne", value=f"{movie_infos.vote_average}/10 par {movie_infos.vote_count} personnes"
        )

        len_overview_movie = len(movie_infos.overview)
        if len_overview_movie > 1020:
            self.add_field(
                name="Synopsis", value=f"{movie_infos.overview[:1020]}...", inline=False
            )
        else:
            self.add_field(
                name="Synopsis", value=f"{movie_infos.overview}", inline=False
            )

        acteurs = "".join(
            f"{acteur} : {charac}\n"
            for acteur, charac in movie_infos.four_main_actor.items()
        )
        self.add_field(
            name="Acteurs principaux", value=acteurs
        )

        if movie_infos.trailer_key:
            self.add_field(
                name="Bande annonce", value=f"https://www.youtube.com/watch?v={movie_infos.trailer_key}", inline=False
            )

    def get_embed(self):
        """
        Get the movie information embed.

        Returns:
            The movie information embed.
        """
        return self


class MovieSelection(discord.ui.Select):
    """
    A class that represents a movie selection dropdown.

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
        """
        Initialize the MovieSelection dropdown.

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
        """
        The callback method that sends a message with movie information when a movie is selected.

        Args:
            interaction: The interaction object.

        Returns:
            None
        """
        movie = self.list_movie[int(self.values[0])]
        await interaction.response.send_message(embed=MovieInfo(movie).get_embed())


class SelectViewMovie(discord.ui.View):
    """
    A class that represents a select view.

    This class extends the discord.ui.View class and provides a view with a movie selection dropdown.
    It takes a list of movies as input and adds a MovieSelection item to the view.

    Args:
        timeout: The timeout duration for the view (default is 60 seconds).
        list_movie: The list of movies to populate the dropdown options.

    Methods:
        None
    """

    def __init__(self, list_movie, timeout=60):
        """
        Initialize the SelectView.

        Args:
            timeout: The timeout duration for the view (default is 60 seconds).
            list_movie: The list of movies to populate the dropdown options.
        """
        super().__init__(timeout=timeout)
        self.add_item(MovieSelection(list_movie))


# ----------------------------- Person ----------------------------------------
class PersonInfo(discord.Embed):
    def __init__(self, person_infos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = person_infos.name
        self.color = discord.Color.from_rgb(69, 44, 129)

        if person_infos.profile_path:
            self.set_thumbnail(
                url=f"https://image.tmdb.org/t/p/w500{person_infos.profile_path}"
            )

        # Birthday
        birthday = person_infos.birthday or "Inconnu"
        self.add_field(
            name="Date de naissance", value=f"{birthday}", inline=True
        )

        # Place of birth
        place_of_birth = person_infos.place_of_birth or "Inconnu"
        self.add_field(
            name="Lieu de naissance", value=place_of_birth, inline=True
        )

        # biography
        if len(person_infos.biography) > 1020:
            self.add_field(
                name="Biographie", value=f"{person_infos.biography[:1020]}...",  inline=False
            )
        else:
            self.add_field(
                name="Biographie", value=f"{person_infos.biography}",  inline=False
            )

        # Played in
        if _ := person_infos.known_for:
            played_in_list = []
            for movie in person_infos.known_for:
                movie_dict = dict(movie)
                try:
                    played_in_list.append(movie_dict["title"])
                except KeyError:
                    with contextlib.suppress(Exception):
                        played_in_list.append(movie_dict["name"])

            played_in = "\n".join(played_in_list)

            self.add_field(
                name="Connus pour :", value=played_in, inline=True
            )
        else:
            self.add_field(
                name="Connus pour :", value="Cette personne n'a pas joué dans un film", inline=True
            )


        # Made movies
        if _ := person_infos.created_movies:
            played_in_list = [film["title"] for film in person_infos.created_movies]
            played_in = "\n".join(played_in_list)

            self.add_field(
                name="A réalisé :", value=played_in, inline=True
            )
        else:
            self.add_field(
                name="Connus pour :", value="Cette personne n'a pas produit de films", inline=True
            )

    def get_embed(self):
        return self

class PersonSelection(discord.ui.Select):
    """
    A class that represents a movie selection dropdown.

    This class extends the discord.ui.Select class and provides a dropdown menu for selecting a movie.
    It takes a list of movies as input and creates options for each movie in the dropdown.

    Args:
        list_movie: The list of movies to populate the dropdown options.

    Attributes:
        list_movie: The list of movies.

    Methods:
        callback: The callback method that sends a message with movie information when a movie is selected.
    """

    def __init__(self, list_person):
        """
        Initialize the MovieSelection dropdown.

        Args:
            list_person: The list of movies to populate the dropdown options.
        """
        options = [
            discord.SelectOption(label=f"{list_person[i].name}", value=f"{i}")
            for i in range(len(list_person))
        ]
        self.list_person = list_person

        super().__init__(
            placeholder="Selectionne une personne pour des informations",
            max_values=1,
            min_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        """
        The callback method that sends a message with movie information when a movie is selected.

        Args:
            interaction: The interaction object.

        Returns:
            None
        """
        person = self.list_person[int(self.values[0])]
        await interaction.response.send_message(embed=PersonInfo(person).get_embed())


class SelectViewPerson(discord.ui.View):
    """
    A class that represents a select view.

    This class extends the discord.ui.View class and provides a view with a movie selection dropdown.
    It takes a list of movies as input and adds a MovieSelection item to the view.

    Args:
        timeout: The timeout duration for the view (default is 60 seconds).
        list_person: The list of movies to populate the dropdown options.

    Methods:
        None
    """

    def __init__(self, list_person, timeout=60):
        super().__init__(timeout=timeout)
        self.add_item(PersonSelection(list_person))

class Search(commands.Cog):
    """
    A class that represents a search music cog.

    This cog provides functionality to search for movies using the TMDB API.
    It includes a method to get the image URL from a movie result and a command to search for movies and display the top 10 results with their posters.

    Args:
        bot: The instance of the bot.

    Attributes:
        bot: The instance of the bot.
        movie: An instance of the Movie class.
    """
    def __init__(self, bot):
        """
        Initialize the SearchMusic cog.

        Args:
            bot: The instance of the bot.
        """
        self.bot = bot
        load_dotenv()
        API_KEY_TMDB = os.getenv("API_KEY_TMDB")
        self.client = Client(API_KEY_TMDB)
        self.info = InfoSearch(self.client)

    @app_commands.command()
    async def search_film(self, interaction: discord.Interaction, nom_du_film: str):
        """
        Search for movies and display the top 10 results with their posters.

        Args:
            interaction: The interaction object.
            nom_du_film: The name of the movie to search for.

        Returns:
            None
        """
        await interaction.response.defer()

        self.result = self.info.search_movies(nom_du_film)
        if self.result:
            top_10_results = self.result[:10]
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

            await interaction.followup.send(
                embed=emb, view=SelectViewMovie(top_10_results)
            )
        else:
            emb_error = discord.Embed(
                title="Pas de resultats",
                color=discord.Color.from_rgb(69, 44, 129),
            )
            emb_error.add_field(
                name=":warning: Erreur :warning:",
                value=f"Aucun film trouvé pour cette recherche: ***{nom_du_film}***"
            )
            await interaction.followup.send(embed=emb_error)

    @app_commands.command()
    async def info_film(self, interaction, nom_du_film: str):
        """
        Search for movies and display the top 10 results with their posters.

        Args:
            interaction: The interaction object.
            nom_du_film: The name of the movie to search for.

        Returns:
            None
        """
        await interaction.response.defer()

        self.result = self.info.search_movies(nom_du_film)
        if self.result:
            top_movie = self.result[0]

            await interaction.followup.send(embed=MovieInfo(top_movie).get_embed())
        else:
            emb_error = discord.Embed(
                title="Pas de resultats",
                color=discord.Color.from_rgb(69, 44, 129),
            )
            emb_error.add_field(
                name=":warning: Erreur :warning:",
                value=f"Aucun film trouvé pour cette recherche: ***{nom_du_film}***"
            )
            await interaction.followup.send(embed=emb_error)

    @app_commands.command()
    async def search_person(self, interaction, nom_de_la_personne: str):
        await interaction.response.defer()

        self.result = self.info.search_persons(nom_de_la_personne)
        if self.result:
            top_10_results = self.result[:10]
            emb = discord.Embed(
                title="Resultats - 10 personnes les plus populaires",
                color=discord.Color.from_rgb(69, 44, 129),
            )
            for i, res in enumerate(top_10_results):
                emb.add_field(
                    name=f"{i+1} - {res.name}",
                    value=f"[Image de : {res.name}](https://image.tmdb.org/t/p/w500{res.profile_path})",
                    inline=False,
                )

            await interaction.followup.send(
                embed=emb, view=SelectViewPerson(top_10_results)
            )
        else:
            emb_error = discord.Embed(
                title="Pas de resultats",
                color=discord.Color.from_rgb(69, 44, 129),
            )
            emb_error.add_field(
                name=":warning: Erreur :warning:",
                value=f"Aucune personne trouvée pour cette recherche: ***{nom_de_la_personne}***"
            )
            await interaction.followup.send(embed=emb_error)
    
    @app_commands.command()
    async def info_person(self, interaction, nom_de_la_personne: str):
        await interaction.response.defer()

        self.result = self.info.search_persons(nom_de_la_personne)
        if self.result:
            top_person = self.result[0]

            await interaction.followup.send(embed=PersonInfo(top_person).get_embed())
        else:
            emb_error = discord.Embed(
                title="Pas de resultats",
                color=discord.Color.from_rgb(69, 44, 129),
            )
            emb_error.add_field(
                name=":warning: Erreur :warning:",
                value=f"Aucune personne trouvé pour cette recherche: ***{nom_de_la_personne}***"
            )
            await interaction.followup.send(embed=emb_error)


async def setup(bot):
    await bot.add_cog(Search(bot))
