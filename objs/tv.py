from babel.dates import format_date
from tmdbv3api import AsObj
import contextlib
import datetime


class TVInfo:
    def __init__(self, tv_infos, tv_details, tv_credits) -> None:
        self.title = tv_infos.get("name", None)
        self.poster_path = tv_infos.get("poster_path", None)
        self.overview = tv_infos.get("overview", None)
        self.vote_average = tv_infos.get("vote_average", None)
        self.vote_count = tv_infos.get("vote_count", None)

        if release_date := tv_infos.get("first_air_date"):
            date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
            self.release_date = format_date(date, format="full", locale="fr_FR").capitalize()

        # creator
        self.creator = "Actuellement pas de createur"
        with contextlib.suppress(Exception):
            self.creator = tv_details["created_by"]

        # cast
        self.cast = tv_details.get("credits", {}).get("cast", [])
        self.four_main_actor = {}

        if len(self.cast) <= 4:
            for actor in self.cast:
                self.four_main_actor[f"{actor['name']}"] = actor.get("character")
        else:
            for i in range(4):
                for actor in self.cast:
                    if int(actor["order"]) == i:
                        self.four_main_actor[f"{actor['name']}"] = actor["character"]

        # trailer
        self.trailer_key = None
        for video in tv_details.get("videos", {}).get("results", []):
            if video["type"] == "Trailer":
                self.trailer_key = video["key"]

        # seasons infos
        self.number_of_seasons = 0
        if tv_details.get("number_of_seasons"):
            for season in tv_details["number_of_seasons"]:
                if season["season_number"] > 0:
                    self.number_of_seasons += 1

        # providers infos
        self.providers = None
        self.flatrate = None
        if tv_details.get("providers", {}).get("results"):
            self.providers = tv_details["providers"]["results"]

            self.flatrate = []
            # on recherche dans la liste des providers le 'result': FR
            for provider in self.providers:
                if provider["results"] == "FR":
                    for item in provider["FR"]:
                        if isinstance(item, AsObj) and item.get("flatrate"):
                            for country_provider in item["flatrate"]:
                                self.flatrate.append(country_provider["provider_name"])
