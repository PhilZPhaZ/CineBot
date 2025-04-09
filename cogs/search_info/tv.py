import discord

class TVInfo(discord.Embed):
    def __init__(self, tv_infos, *args, **kwargs):
        """
        Initialize the TVInfo embed.

        Args:
            movie_infos: The movie information object.
            *args: Additional arguments to pass to the discord.Embed constructor.
            **kwargs: Additional keyword arguments to pass to the discord.Embed constructor.
        """
        super().__init__(*args, **kwargs)
        self.title = tv_infos.title
        self.color = discord.Color.from_rgb(69, 44, 129)

        self.set_thumbnail(
            url=f"https://image.tmdb.org/t/p/w500{tv_infos.poster_path}"
        )

        if tv_infos.release_date:
            self.add_field(
                name="Date de sortie", value=f"{tv_infos.release_date}", inline=True
            )
        else:
            self.add_field(
                name="Date de sortie", value="A determiner | Inconnue", inline=True
            )

        # creator(s)
        creators = "\n".join([person["name"] for person in tv_infos.creator])
        self.add_field(
            name="Createur(s)", value=creators, inline=True
        )

        self.add_field(
            name="Note moyenne", value=f"{tv_infos.vote_average}/10 par {tv_infos.vote_count} personnes"
        )

        len_overview_movie = len(tv_infos.overview)
        if len_overview_movie > 1020:
            self.add_field(
                name="Synopsis", value=f"{tv_infos.overview[:1020]}...", inline=False
            )
        else:
            self.add_field(
                name="Synopsis", value=f"{tv_infos.overview}", inline=False
            )

        self.add_field(
            name="Nombre de saisons", value=f"{tv_infos.number_of_seasons}", inline=False
        )

        acteurs = "".join(
            f"{acteur} : {charac}\n"
            for acteur, charac in tv_infos.four_main_actor.items()
        )
        self.add_field(
            name="Acteurs principaux", value=acteurs
        )
        
        # providers
        flatrate_providers = "\n".join(
            f"{name}" for name in tv_infos.flatrate
        )
        if flatrate_providers:
            self.add_field(
                name="Streaming", value=flatrate_providers, inline=True
            )
        else:
            self.add_field(
                name="Streaming", value="Pas de plateforme de streaming disponible", inline=False
            )

        # trailer
        if tv_infos.trailer_key:
            self.add_field(
                name="Bande annonce", value=f"https://www.youtube.com/watch?v={tv_infos.trailer_key}", inline=False
            )

    def get_embed(self):
        """
        Get the movie information embed.

        Returns:
            The movie information embed.
        """
        return self
