from .movie import MovieInfo
from .person import PersonInfo
from .tv import TVInfo
from utils import create_error_embed
import discord


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


class MovieRecommendation(discord.ui.Select):
    """
    A class that represents a movie recommendation dropdown.

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
        Initialize the MovieRecommendation dropdown.

        Args:
            list_movie: The list of movies to populate the dropdown options.
        """
        options = [
            discord.SelectOption(label=f"{list_movie[i].title}", value=f"{i}")
            for i in range(len(list_movie))
        ]
        self.list_movie = list_movie

        super().__init__(
            placeholder="Recommendations",
            max_values=1,
            min_values=1,
            options=options,
        )
    
    async def callback(self, interaction: discord.Interaction):
        """
        The callback method that handles movie recommendation selection.
        """
        # Defer the response immediately
        await interaction.response.defer()

        # Get selected movie
        movie = self.list_movie[int(self.values[0])]

        # Get Search cog
        search_cog = interaction.client.get_cog("Search")
        if search_cog:
            try:
                # Access the search functionality directly instead of using the command
                result = search_cog.info.search_movies(movie.title)
                if result:
                    top_movie = result[0]
                    # Send the movie info with a new recommendation view
                    await interaction.followup.send(
                        embed=MovieInfo(top_movie).get_embed(), 
                        view=RecommendationViewMovie(top_movie.recommendations)
                    )
                else:
                    await interaction.followup.send(
                        embed=create_error_embed(
                            title="Pas de resultats",
                            description=f"Aucun film trouvé pour cette recherche: ***{movie.title}***"
                        )
                    )
            except Exception as e:
                await interaction.followup.send(
                    embed=create_error_embed(
                        title="Erreur Interne",
                        description=f"Une erreur s'est produite lors de la recherche: {str(e)}"
                    )
                )
        else:
            await interaction.followup.send(
                embed=create_error_embed(
                    title="Pas de resultats",
                    description=f"Aucun film trouvé pour cette recherche: ***{movie.title}***"
                )
            )


class RecommendationViewMovie(discord.ui.View):
    """
    A class that represents a recommendation view.

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
        Initialize the RecommendationViewMovie.

        Args:
            timeout: The timeout duration for the view (default is 60 seconds).
            list_movie: The list of movies to populate the dropdown options.
        """
        super().__init__(timeout=timeout)
        self.add_item(MovieRecommendation(list_movie))

        
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
        """
        Summary: Represents a class for searching.

        Explanation: This class is used for searching, but the provided code snippet is incomplete and does not provide further details for the class.

        Args: None

        Returns: None
        """

        super().__init__(timeout=timeout)
        self.add_item(PersonSelection(list_person))



class TVSelection(discord.ui.Select):
    """
    A custom UI component for selecting a TV series from a list.

    Args:
        list_tv (list): A list of TV series objects to populate the selection options.

    Returns:
        None

    Raises:
        No specific exceptions are raised.
    """
    def __init__(self, list_tv):
        options = [
            discord.SelectOption(label=f"{list_tv[i].title}", value=f"{i}")
            for i in range(len(list_tv))
        ]
        self.list_movie = list_tv

        super().__init__(
            placeholder="Selectionne une série pour des informations",
            max_values=1,
            min_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        movie = self.list_movie[int(self.values[0])]
        await interaction.response.send_message(embed=TVInfo(movie).get_embed())


class SelectViewTV(discord.ui.View):
    """
    Initialize a UI component with a list of movies for selection.

    Args:
        list_movie (list): A list of movie objects to populate the selection.
        timeout (int, optional): Timeout value for the UI component in seconds. Defaults to 60.

    Returns:
        None

    Raises:
        No specific exceptions are raised.
    """
    def __init__(self, list_movie, timeout=60):
        super().__init__(timeout=timeout)
        self.add_item(TVSelection(list_movie))


class TVRecommendations(discord.ui.Select):
    """
    A class that represents a movie recommendation dropdown.

    This class extends the discord.ui.Select class and provides a dropdown menu for selecting a movie.
    It takes a list of movies as input and creates options for each movie in the dropdown.

    Args:
        list_movie: The list of movies to populate the dropdown options.

    Attributes:
        list_movie: The list of movies.

    Methods:
        callback: The callback method that sends a message with movie information when a movie is selected.
    """

    def __init__(self, list_tv):
        """
        Initialize the MovieRecommendation dropdown.

        Args:
            list_tv: The list of movies to populate the dropdown options.
        """
        options = [
            discord.SelectOption(label=f"{list_tv[i].name}", value=f"{i}")
            for i in range(len(list_tv))
        ]
        self.list_tv = list_tv

        super().__init__(
            placeholder="Recommendations",
            max_values=1,
            min_values=1,
            options=options,
        )
    
    async def callback(self, interaction: discord.Interaction):
        """
        The callback method that handles movie recommendation selection.
        """
        # Defer the response immediately
        await interaction.response.defer()

        # Get selected movie
        tv = self.list_tv[int(self.values[0])]

        # Get Search cog
        search_cog = interaction.client.get_cog("Search")
        if search_cog:
            try:
                # Access the search functionality directly instead of using the command
                result = search_cog.info.search_tv(tv.name)
                if result:
                    top_tv = result[0]
                    # Send the tv info with a new recommendation view
                    await interaction.followup.send(
                        embed=TVInfo(top_tv).get_embed(), 
                        view=RecommendationViewTV(top_tv.recommendations)
                    )
                else:
                    await interaction.followup.send(
                        embed=create_error_embed(
                            title="Pas de resultats",
                            description=f"Aucun film trouvé pour cette recherche: ***{tv.title}***"
                        )
                    )
            except Exception as e:
                await interaction.followup.send(
                    embed=create_error_embed(
                        title="Erreur Interne",
                        description=f"Une erreur s'est produite lors de la recherche: {str(e)}"
                    )
                )
        else:
            await interaction.followup.send(
                embed=create_error_embed(
                    title="Pas de resultats",
                    description=f"Aucun film trouvé pour cette recherche: ***{tv.title}***"
                )
            )


class RecommendationViewTV(discord.ui.View):
    """
    A class that represents a recommendation view.

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
        Initialize the RecommendationViewMovie.

        Args:
            timeout: The timeout duration for the view (default is 60 seconds).
            list_movie: The list of movies to populate the dropdown options.
        """
        super().__init__(timeout=timeout)
        self.add_item(TVRecommendations(list_movie))

