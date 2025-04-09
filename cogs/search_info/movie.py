import discord

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

        if movie_infos.poster_path:
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
        if acteurs:
            self.add_field(
                name="Acteurs principaux", value=acteurs
            )
        else:
            self.add_field(
                name="Acteurs principaux", value="Pas d'acteurs principaux disponibles"
            )

        flatrate_providers = "\n".join(
            f"{name}" for name in movie_infos.flatrate
        )
        if flatrate_providers:
            self.add_field(
                name="Streaming", value=flatrate_providers, inline=True
            )
        else:
            self.add_field(
                name="Streaming", value="Pas de plateforme de streaming disponible", inline=False
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
