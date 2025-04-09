from babel.dates import format_date
from tmdbv3api import AsObj
import datetime


class MovieInfo:
    """
    Represents movie information.

    Args:
        movie_info (dict): A dictionary containing general movie information.
        movie_details (dict): A dictionary containing additional movie details.
        movie_videos_info (obj): An object containing movie video information.

    Attributes:
        title (str): The title of the movie.
        poster_path (str): The path to the movie's poster image.
        overview (str): A brief overview of the movie.
        vote_average (float): The average vote rating for the movie.
        vote_count (int): The number of votes for the movie.
        release_date (str): The formatted release date of the movie.
        details (dict): Additional details about the movie.
        director (str): The name of the movie's director.
        cast (list): A list of cast members in the movie.
        four_main_actor (dict): A dictionary containing the names of the four main actors and their corresponding characters.
        trailer_key (str): The key of the movie's trailer video.

    Raises:
        None

    Examples:
        None
    """
    def __init__(self, movie_info, movie_details, movie_videos_info) -> None:
        # general
        self.title = movie_info.get("title", None)
        self.poster_path = movie_info.get("poster_path", None)
        self.overview = movie_info.get("overview", None)
        self.vote_average = movie_info.get("vote_average", None)
        self.vote_count = movie_info.get("vote_count", None)

        if release_date := movie_info.get("release_date"):
            try:
                date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
                self.release_date = format_date(date, format="full", locale="fr_FR").capitalize()
            except ValueError:
                self.release_date = "Date de sortie inconnue"
        else:
            self.release_date = "Date de sortie inconnue"

        # cast
        self.details = movie_details

        # Realisateur
        self.director = "Pas de realisateur"
        if self.details.get("casts", {}).get("crew"):
            for person in self.details["casts"]["crew"]:
                if person["job"] == "Director":
                    self.director = person["name"]
                    break

        self.cast = movie_details.get("casts", {}).get("cast", [])
        self.four_main_actor = {}

        if len(self.cast) <= 4:
            for actor in self.cast:
                self.four_main_actor[f"{actor['name']}"] = actor["character"]
        else:
            for i in range(4):
                for actor in self.cast:
                    if int(actor["order"]) == i:
                        self.four_main_actor[f"{actor['name']}"] = actor["character"]

        # video
        self.trailer_key = None
        for video in movie_videos_info.results:
            if video["type"] == 'Trailer':
                self.trailer_key = video["key"]
        
        self.providers = None
        self.flatrate = None
        if self.details.get("providers", {}).get("results"):
            self.providers = self.details.get("providers", {}).get("results")

            self.flatrate = []
            # on recherche dans la liste des providers le 'result': FR
            for provider in self.providers:
                if provider["results"] == "FR":
                    for item in provider["FR"]:
                        if isinstance(item, AsObj) and item.get("flatrate"):
                            for country_provider in item["flatrate"]:
                                self.flatrate.append(country_provider["provider_name"])
