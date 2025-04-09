import discord
import contextlib

class PersonInfo(discord.Embed):
    """
    Summary: Represents a Discord embed for displaying information about a person.

    Explanation: Initializes a Discord embed with information about a person, including their name, profile picture, birthday, place of birth, biography, movies they played in, and movies they created. Provides a method to retrieve the embed.

    Args:
    - person_infos: Information about the person.
    - *args: Additional arguments for the Discord embed.
    - **kwargs: Additional keyword arguments for the Discord embed.

    Returns:
    - Discord embed: An embed containing the person's information.
    """
    def __init__(self, person_infos, *args, **kwargs):
        """
        Summary: Initializes a new instance of a class with provided person information and additional arguments.

        Explanation: Constructor for the class that initializes a new instance with person information and any additional arguments passed to it.

        Args:
        - person_infos: Information about the person.
        - *args: Additional positional arguments.
        - **kwargs: Additional keyword arguments.

        Returns: None
        """
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
                except Exception:
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
            played_in_list = []

            for film in person_infos.created_movies:
                try:
                    played_in_list.append(film["title"])
                except Exception:
                    with contextlib.suppress(KeyError):
                        played_in_list.append(film["name"])

            played_in = "\n".join(played_in_list)

            self.add_field(
                name="A réalisé :", value=played_in, inline=True
            )
        else:
            self.add_field(
                name="Connus pour :", value="Cette personne n'a pas produit de films", inline=True
            )

    def get_embed(self):
        """
        Summary: Represents a class for selecting a person.

        Explanation: This class is used for selecting a person, but the provided code snippet is incomplete and does not provide further details for the class.

        Args: None

        Returns: None
        """
        return self
