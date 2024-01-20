from tmdbv3api import TMDb, Movie, Person
import datetime

class MovieInfo:
    def __init__(self, movie_info, movie_details, movie_videos_info) -> None:
        # general
        self.title = movie_info["title"]
        self.poster_path = movie_info["poster_path"]
        self.overview = movie_info["overview"]
        self.vote_average = movie_info["vote_average"]
        self.vote_count = movie_info["vote_count"]
        
        release_date = movie_info["release_date"]
        date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
        self.release_date = date.strftime("%A %d %B %Y").capitalize()

        # cast
        self.details = movie_details

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


class MovieSearch(Movie, Person):
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

    def search(self, query):
        """Search for movies.

        Args:
            query: The query string to search for.

        Returns:
            The search results.

        """     
        return_list = []

        movies = self.search_movies(query)
        movies_list = list(movies)

        for res in movies_list:
            movie_id = res["id"]
            
            # get movie video infos
            movie_videos_info = self.videos(movie_id)

            movie_details = self.get_details(movie_id)

            new_film = MovieInfo(res, movie_details, movie_videos_info)
            return_list.append(new_film)

        return return_list
    
    def get_details(self, id):
        return self.details(id)
