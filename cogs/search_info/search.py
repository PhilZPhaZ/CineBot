from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from .views import SelectViewMovie, SelectViewPerson, SelectViewTV, RecommendationViewMovie, RecommendationViewTV
from utils import create_error_embed
from cinebot import InfoSearch, Client
from .movie import MovieInfo
from .person import PersonInfo
from .tv import TVInfo
import os
import discord


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

        try:
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
                await interaction.followup.send(
                    embed=create_error_embed(
                        title="Pas de resultats",
                        description=f"Aucun film trouvé pour cette recherche: ***{nom_du_film}***"
                    )
                )
        except Exception as e:
            await interaction.followup.send(
                embed=create_error_embed(
                    title="Erreur Interne",
                    description=f"Une erreur s'est produite lors de la recherche: {str(e)}"
                )
            )

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

        try:
            self.result = self.info.search_movies(nom_du_film)
            if self.result:
                top_movie = self.result[0]

                await interaction.followup.send(embed=MovieInfo(top_movie).get_embed(), view=RecommendationViewMovie(top_movie.recommendations))
            else:
                await interaction.followup.send(
                    embed=create_error_embed(
                        title="Pas de resultats",
                        description=f"Aucun film trouvé pour cette recherche: ***{nom_du_film}***"
                    )
                )
        except Exception as e:
            await interaction.followup.send(
                embed=create_error_embed(
                    title="Erreur Interne",
                    description=f"Une erreur s'est produite lors de la recherche: {str(e)}"
                )
            )

    @app_commands.command()
    async def search_person(self, interaction, nom_de_la_personne: str):
        """
        Summary: Command function for searching a person.

        Explanation: Handles the search for a person based on the provided name. Displays the top 10 most popular results with their names and profile images in an embed. If no results are found, an error message is displayed.

        Args:
        - interaction: The interaction object.
        - nom_de_la_personne: The name of the person to search for.

        Returns: None
        """
        await interaction.response.defer()

        try:
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
                await interaction.followup.send(
                    embed=create_error_embed(
                        title="Pas de resultats",
                        description=f"Aucune personne trouvée pour cette recherche: ***{nom_de_la_personne}***"
                    )
                )
        except Exception as e:
            await interaction.followup.send(
                embed=create_error_embed(
                    title="Erreur Interne",
                    description=f"Une erreur s'est produite lors de la recherche: {str(e)}"
                )
            )
    
    @app_commands.command()
    async def info_person(self, interaction, nom_de_la_personne: str):
        """
        Summary: Asynchronous function for retrieving information about a person.

        Explanation: Retrieves information about a person based on the provided name. Sends an embed with the person's details if found, otherwise sends an error message.

        Args:
        - interaction: The interaction object.
        - nom_de_la_personne: The name of the person to retrieve information for.

        Returns: None
        """
        await interaction.response.defer()

        try:
            self.result = self.info.search_persons(nom_de_la_personne)
            if self.result:
                top_person = self.result[0]

                await interaction.followup.send(embed=PersonInfo(top_person).get_embed())
            else:
                await interaction.followup.send(
                    embed=create_error_embed(
                        title="Pas de resultats",
                        description=f"Aucune personne trouvée pour cette recherche: ***{nom_de_la_personne}***"
                    )
                )
        except Exception as e:
            await interaction.followup.send(
                embed=create_error_embed(
                    title="Erreur Interne",
                    description=f"Une erreur s'est produite lors de la recherche: {str(e)}"
                )
            )
    
    @app_commands.command()
    async def search_serie(self, interaction, nom_de_la_serie: str):
        """
        Search for a TV series and display the top 10 most popular results.

        Args:
            nom_de_la_serie (str): The name of the TV series to search for.

        Returns:
            None

        Raises:
            No specific exceptions are raised.

        Examples:
            None
        """
        await interaction.response.defer()
        
        try:
            self.result = self.info.search_tv(nom_de_la_serie)
            if self.result:
                top_10_results = self.result[:10]
                emb = discord.Embed(
                    title="Resultats - 10 séries les plus populaires",
                    color=discord.Color.from_rgb(69, 44, 129),
                )
                for i, res in enumerate(top_10_results):
                    emb.add_field(
                        name=f"{i+1} - {res.title}",
                        value=f"[Image de : {res.title}](https://image.tmdb.org/t/p/w500{res.poster_path})",
                        inline=False,
                    )

                await interaction.followup.send(
                    embed=emb, view=SelectViewTV(top_10_results)
                )
            else:
                await interaction.followup.send(
                    embed=create_error_embed(
                        title="Pas de resultats",
                        description=f"Aucune série trouvée pour cette recherche: ***{nom_de_la_serie}***"
                    )
                )
        except Exception as e:
            await interaction.followup.send(
                embed=create_error_embed(
                    title="Erreur Interne",
                    description=f"Une erreur s'est produite lors de la recherche: {str(e)}"
                )
            )
    
    @app_commands.command()
    async def info_serie(self, interaction, nom_de_la_serie: str):
        """
        Retrieve information about a specific TV series and send it as an embed.

        Args:
            interaction: The interaction object.
            nom_de_la_serie (str): The name of the TV series to retrieve information for.

        Returns:
            None

        Raises:
            No specific exceptions are raised.
        """
        await interaction.response.defer()

        try:
            self.result = self.info.search_tv(nom_de_la_serie)
            if self.result:
                top_tv = self.result[0]
                await interaction.followup.send(embed=TVInfo(top_tv).get_embed(), view=RecommendationViewTV(top_tv.recommendations))
            else:
                await interaction.followup.send(
                    embed=create_error_embed(
                        title="Pas de resultats",
                        description=f"Aucune série trouvée pour cette recherche: ***{nom_de_la_serie}***"
                    )
                )
        except Exception as e:
            await interaction.followup.send(
                embed=create_error_embed(
                    title="Erreur Interne",
                    description=f"Une erreur s'est produite lors de la recherche: {str(e)}"
                )
            )


async def setup(bot):
    await bot.add_cog(Search(bot))
