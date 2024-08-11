import contextlib
from tmdbv3api import TMDb, Movie, Person, TV
from babel.dates import format_date
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
        self.title = movie_info["title"]
        self.poster_path = movie_info["poster_path"]
        self.overview = movie_info["overview"]
        self.vote_average = movie_info["vote_average"]
        self.vote_count = movie_info["vote_count"]

        if release_date := movie_info["release_date"]:
            date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
            self.release_date = format_date(date, format="full", locale="fr_FR").capitalize()

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
    """
    Summary: Represents a class for storing information about a person.

    Explanation: Initializes the class with details about a person, including their name, profile path, jobs, birthday, place of birth, top 5 known movies, top 5 created movies, and biography. The class provides methods for sorting movies based on vote count and average.

    Args:
    - person_info: Information about the person.
    - infos: Additional details about the person.
    - person_details: Details about the person's movies and biography.

    Returns: None
    """
    def __init__(self, person_info, infos, person_details) -> None:
        self.name = person_info["name"]
        self.profile_path = person_info["profile_path"]
        self.jobs = infos["known_for_department"]

        # Birthday
        if birthday := infos["birthday"]:
            date = datetime.datetime.strptime(birthday, "%Y-%m-%d")
            self.birthday = format_date(date, format="full", locale="fr_FR").capitalize()

        # Place of birth
        if place_of_birth := infos["place_of_birth"]:
            self.place_of_birth = place_of_birth

        # 5 best movies
        try:
            all_movies = list(person_details["cast"])

            self.known_for = sorted(all_movies, key=lambda x: self.best_ratio_for_movie(x["vote_count"], x["vote_average"]), reverse=True)
            if len(self.known_for) > 5:
                self.known_for = self.known_for[:5]
        except Exception:
            self.known_for = None
        
        # 5 best created movies
        try:
            all_movies = list(person_details["crew"])

            self.created_movies = sorted(all_movies, key=lambda x: self.best_ratio_for_movie(x["vote_count"], x["vote_average"]), reverse=True)

            # enlever les doublons
            final_list = []
            name_list = []
            for movie in self.created_movies:
                if movie["id"] not in name_list:
                    final_list.append(movie)
                    name_list.append(movie["id"])
            
            self.created_movies = final_list
            
            if len(self.created_movies) > 5:
                self.created_movies = self.created_movies[:5]
        except Exception:
            self.created_movies = None


        # biography
        try:
            self.biography = infos["biography"]
        except Exception:
            self.biography = "Pas de biographie"

    def best_ratio_for_movie(self, vote_count, vote):
        return vote * vote_count


class TVInfo:
    def __init__(self, tv_infos, tv_details, tv_credits) -> None:
        self.title = tv_infos["name"]
        self.poster_path = tv_infos["poster_path"]
        self.overview = tv_infos["overview"]
        self.vote_average = tv_infos["vote_average"]
        self.vote_count = tv_infos["vote_count"]

        if release_date := tv_infos["first_air_date"]:
            date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
            self.release_date = format_date(date, format="full", locale="fr_FR").capitalize()

        # creator
        self.creator = "Actuellement pas de createur"
        with contextlib.suppress(Exception):
            self.creator = tv_details["created_by"]

        # cast
        self.cast = tv_details["credits"]["cast"]
        self.four_main_actor = {}

        if len(self.cast) <= 4:
            for actor in self.cast:
                self.four_main_actor[f"{actor['name']}"] = actor["character"]
        else:
            for i in range(4):
                for actor in self.cast:
                    if int(actor["order"]) == i:
                        self.four_main_actor[f"{actor['name']}"] = actor["character"]

        # trailer
        self.trailer_key = None
        for video in tv_details["videos"]["results"]:
            if video["type"] == "Trailer":
                self.trailer_key = video["key"]
        
        # seasons infos
        self.number_of_seasons = 0
        for season in tv_details["seasons"]:
            if season["season_number"] > 0:
                self.number_of_seasons += 1


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

                new_film = MovieInfo(res, movie_details, movie_videos_info)
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
        try:
            return_list = []
            
            tvs = self.get_tv_infos(query)
            tvs_list = list(tvs)

            for res in tvs_list:
                tv_id = res["id"]

                tv_details = self.details_tv(tv_id)
                tv_credits = self.credits_tv(tv_id)

                new_tv = TVInfo(res, tv_details, tv_credits)
                return_list.append(new_tv)
            return return_list
        except Exception:
            return None