from tmdbv3api import TMDb, Movie, Person
import datetime
import json


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
        self.title = movie_info["title"]
        self.poster_path = movie_info["poster_path"]
        self.overview = movie_info["overview"]
        self.vote_average = movie_info["vote_average"]
        self.vote_count = movie_info["vote_count"]

        if release_date := movie_info["release_date"]:
            date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
            self.release_date = date.strftime("%A %d %B %Y").capitalize()

        # cast
        self.details = movie_details

        # Realisateur
        self.director = "Pas de realisateur"
        for person in self.details["casts"]["crew"]:
            if person["job"] == "Director":
                self.director = person["name"]

        self.cast = movie_details["casts"]["cast"]
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


class PersonInfo:
    def __init__(self, person_info, person_details) -> None:
        self.name = person_info["name"]
        self.profile_path = person_info["profile_path"]

        self.details = person_details


class Client(TMDb):
    """A class that represents a TMDB client.

    This class extends the TMDb class and provides additional functionality for the CineBot application.
    It initializes the client with the provided API key and language.

    Args:
        api_key: The API key for TMDB.
        language: The language to use for the client (default is "fr").

    Attributes:
        api_key: The API key for TMDB.
        language: The language to use for the client.

    """

    def __init__(self, api_key, language="fr"):
        """Initialize the TMDB client.

        Args:
            api_key: The API key for TMDB.
            language: The language to use for the client (default is "fr").

        """
        super().__init__()
        self.api_key = api_key
        self.language = language


class InfoSearch(Movie, Person):
    """A class that represents a movie.

    This class extends the Client and Movie classes and provides additional functionality for searching movies.
    It inherits the search method from the Movie class.

    Args:
        api_key: The API key for TMDB.
        language: The language to use for the client (default is "fr").

    Attributes:
        api_key: The API key for TMDB.
        language: The language to use for the client.

    """

    def __init__(self, client):
        """Initialize the Movie object.

        Args:
            api_key: The API key for TMDB.
            language: The language to use for the client (default is "fr").

        """
        Movie.__init__(self, client)
        Person.__init__(self, client)

    def search_movies(self, query):
        """Search for movies.

        Args:
            query: The query string to search for.

        Returns:
            The search results.

        """
        try:
            return_list = []

            movies = self.get_movie_infos(query)
            movies_list = list(movies)

            for res in movies_list:
                movie_id = res["id"]

                # get movie video infos
                movie_videos_info = self.videos(movie_id)

                movie_details = self.get_details_film(movie_id)

                new_film = MovieInfo(res, movie_details, movie_videos_info)
                return_list.append(new_film)
            return return_list
        except Exception:
            return None

    def get_details_film(self, id):
        return self.details_film(id)

    def search_persons(self, query):
        try:
            return_list = []

            persons = self.get_person_infos(query)
            persons_list = list(persons)

            for res in persons_list:
                person_id = res['id']
                
                person_details = self.get_details_person(int(person_id))
            
                new_person = PersonInfo(res, person_details)
                return_list.append(new_person)
            return return_list
        except Exception:
            return None
    
    def get_details_person(self, id):
        return self.combined_credits_person(id)

