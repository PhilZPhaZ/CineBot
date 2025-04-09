from babel.dates import format_date
import datetime


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
        self.name = person_info.get("name", None)
        self.profile_path = person_info.get("profile_path", None)
        self.jobs = infos.get("known_for_department", None)

        # Birthday
        if birthday := infos.get("birthday"):
            date = datetime.datetime.strptime(birthday, "%Y-%m-%d")
            self.birthday = format_date(date, format="full", locale="fr_FR").capitalize()
        else:
            self.birthday = "Date de naissance inconnue"

        # Place of birth
        if place_of_birth := infos.get("place_of_birth"):
            self.place_of_birth = place_of_birth
        else:
            self.place_of_birth = "Lieu de naissance inconnu"

        # 5 best movies
        try:
            all_movies = list(person_details.get("cast", []))

            self.known_for = sorted(all_movies, key=lambda x: self.best_ratio_for_movie(x["vote_count"], x["vote_average"]), reverse=True)
            if len(self.known_for) > 5:
                self.known_for = self.known_for[:5]
        except Exception:
            self.known_for = None
        
        # 5 best created movies
        try:
            all_movies = list(person_details.get("crew", []))

            self.created_movies = sorted(all_movies, key=lambda x: self.best_ratio_for_movie(x["vote_count"], x["vote_average"]), reverse=True)

            # enlever les doublons
            final_list = []
            name_list = []
            for movie in self.created_movies:
                if movie["id"] not in name_list:
                    final_list.append(movie)
                    name_list.append(movie.get("id"))

            self.created_movies = final_list

            if len(self.created_movies) > 5:
                self.created_movies = self.created_movies[:5]
        except Exception:
            self.created_movies = None


        # biography
        self.biography = infos.get("biography", None)
        if self.biography is None:
            self.biography = "Pas de biographie"

    def best_ratio_for_movie(self, vote_count, vote):
        return vote * vote_count
