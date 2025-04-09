from tmdbv3api import TMDb, Movie, Person, TV
from objs import MovieInfo, PersonInfo, TVInfo

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


class InfoSearch(Movie, Person, TV):
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
        TV.__init__(self, client)

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
                movie_details = self.details_film(movie_id)
                movie_details.providers = self.watch_providers_movie(movie_id)

                # recommendations
                movie_recommendations = self.recommendations_movie(movie_id)

                new_film = MovieInfo(res, movie_details, movie_videos_info, movie_recommendations)
                return_list.append(new_film)
            return return_list
        except Exception:
            return None

    def search_persons(self, query):
        """
        Summary: Retrieves detailed information about multiple persons.

        Explanation: Retrieves and combines information about multiple persons based on the provided query. Creates instances of PersonInfo for each person and returns a list of the gathered information.

        Args:
        - query: The query used to search for persons.

        Returns:
        - List: A list of PersonInfo instances for each person found, or None if an exception occurs.
        """
        try:
            return_list = []

            persons = self.get_person_infos(query)
            persons_list = list(persons)

            for res in persons_list:
                person_id = res['id']

                person_infos = self.get_infos_from_the_person(int(person_id))
                person_details = self.combined_credits_person(int(person_id))

                new_person = PersonInfo(res, person_infos, person_details)
                return_list.append(new_person)
            return return_list
        except Exception:
            return None
    
    def search_tv(self, query):
        return_list = []
        
        tvs = self.get_tv_infos(query)
        tvs_list = list(tvs)

        for res in tvs_list:
            tv_id = res["id"]

            tv_details = self.details_tv(tv_id)
            tv_details.providers = self.watch_providers_tv(tv_id)
            tv_credits = self.credits_tv(tv_id)

            # recommendations
            tv_recommendations = self.recommendations_tv(tv_id)

            new_tv = TVInfo(res, tv_details, tv_credits, tv_recommendations)
            return_list.append(new_tv)
        return return_list