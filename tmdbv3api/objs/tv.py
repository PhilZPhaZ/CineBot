from tmdbv3api.tmdb import TMDb
from .search import Search

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


class TV(TMDb):
    _urls_tv = {
        "details": "/tv/%s",
        "account_states": "/tv/%s/account_states",
        "aggregate_credits": "/tv/%s/aggregate_credits",
        "alternative_titles": "/tv/%s/alternative_titles",
        "changes": "/tv/%s/changes",
        "content_ratings": "/tv/%s/content_ratings",
        "credits": "/tv/%s/credits",
        "episode_groups": "/tv/%s/episode_groups",
        "external_ids": "/tv/%s/external_ids",
        "images": "/tv/%s/images",
        "keywords": "/tv/%s/keywords",
        "recommendations": "/tv/%s/recommendations",
        "reviews": "/tv/%s/reviews",
        "screened_theatrically": "/tv/%s/screened_theatrically",
        "similar": "/tv/%s/similar",
        "translations": "/tv/%s/translations",
        "videos": "/tv/%s/videos",
        "watch_providers": "/tv/%s/watch/providers",
        "rate_tv_show": "/tv/%s/rating",
        "delete_rating": "/tv/%s/rating",
        "latest": "/tv/latest",
        "airing_today": "/tv/airing_today",
        "on_the_air": "/tv/on_the_air",
        "popular": "/tv/popular",
        "top_rated": "/tv/top_rated",
    }

    def details_tv(self, tv_id, append_to_response="videos,trailers,images,credits,translations"):
        """
        Get the primary TV show details by id.
        :param tv_id: int
        :param append_to_response: str
        :return:
        """
        return self._request_obj(
            self._urls_tv["details"] % tv_id,
            params="append_to_response=%s" % append_to_response,
        )

    def account_states(self, tv_id):
        """
        Grab the following account states for a session:
        TV show rating, If it belongs to your watchlist, or If it belongs to your favourite list.
        :param tv_id: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["account_states"] % tv_id,
            params="session_id=%s" % self.session_id
        )

    def aggregate_credits(self, tv_id):
        """
        Get the aggregate credits (cast and crew) that have been added to a TV show.
        This call differs from the main credits call in that it does not return the newest season but rather,
        is a view of all the entire cast & crew for all episodes belonging to a TV show.
        :param tv_id: int
        :return:
        """
        return self._request_obj(self._urls_tv["aggregate_credits"] % tv_id)

    def alternative_titles_tv(self, tv_id):
        """
        Returns all of the alternative titles for a TV show.
        :param tv_id: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["alternative_titles"] % tv_id,
            key="results"
        )

    def changes(self, tv_id, start_date=None, end_date=None, page=1):
        """
        Get the changes for a TV show. By default only the last 24 hours are returned.
        You can query up to 14 days in a single query by using the start_date and end_date query parameters.
        :param tv_id: int
        :param start_date: str
        :param end_date: str
        :param page: int
        """
        params = "page=%s" % page
        if start_date:
            params += "&start_date=%s" % start_date
        if end_date:
            params += "&end_date=%s" % end_date
        return self._request_obj(
            self._urls_tv["changes"] % tv_id,
            params=params,
            key="changes"
        )

    def content_ratings(self, tv_id):
        """
        Get the list of content ratings (certifications) that have been added to a TV show.
        :param tv_id: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["content_ratings"] % tv_id,
            key="results"
        )

    def credits_tv(self, tv_id):
        """
        Get the credits (cast and crew) that have been added to a TV show.
        :param tv_id: int
        :return:
        """
        return self._request_obj(self._urls_tv["credits"] % tv_id)

    def episode_groups(self, tv_id):
        """
        Get all of the episode groups that have been created for a TV show.
        :param tv_id: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["episode_groups"] % tv_id,
            key="results"
        )

    def external_ids(self, tv_id):
        """
        Get the external ids for a TV show.
        :param tv_id: int
        :return:
        """
        return self._request_obj(self._urls_tv["external_ids"] % tv_id)

    def images_tv(self, tv_id, include_image_language=None):
        """
        Get the images that belong to a TV show.
        Querying images with a language parameter will filter the results.
        If you want to include a fallback language (especially useful for backdrops)
        you can use the include_image_language parameter.
        This should be a comma separated value like so: include_image_language=en,null.
        :param tv_id: int
        :param include_image_language: str
        :return:
        """
        return self._request_obj(
            self._urls_tv["images"] % tv_id,
            params="include_image_language=%s" % include_image_language if include_image_language else ""
        )

    def keywords_tv(self, tv_id):
        """
        Get the keywords that have been added to a TV show.
        :param tv_id: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["keywords"] % tv_id,
            key="results"
        )

    def recommendations_tv(self, tv_id, page=1):
        """
        Get the list of TV show recommendations for this item.
        :param tv_id: int
        :param page: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["recommendations"] % tv_id,
            params="page=%s" % page,
            key="results"
        )

    def reviews(self, tv_id, page=1):
        """
        Get the reviews for a TV show.
        :param tv_id: int
        :param page: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["reviews"] % tv_id,
            params="page=%s" % page,
            key="results"
        )

    def screened_theatrically(self, tv_id):
        """
        Get a list of seasons or episodes that have been screened in a film festival or theatre.
        :param tv_id: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["screened_theatrically"] % tv_id,
            key="results"
        )

    def similar_tv(self, tv_id, page=1):
        """
        Get the primary TV show details by id.
        :param tv_id: int
        :param page: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["similar"] % tv_id,
            params="page=%s" % page,
            key="results"
        )

    def translations(self, tv_id):
        """
        Get a list of the translations that exist for a TV show.
        :param tv_id: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["translations"] % tv_id,
            key="translations"
        )

    def videos_tv(self, tv_id, include_video_language=None, page=1):
        """
        Get the videos that have been added to a TV show.
        :param tv_id: int
        :param include_video_language: str
        :param page: int
        :return:
        """
        params = "page=%s" % page
        if include_video_language:
            params += "&include_video_language=%s" % include_video_language
        return self._request_obj(
            self._urls_tv["videos"] % tv_id,
            params=params
        )

    def watch_providers_tv(self, tv_id):
        """
        You can query this method to get a list of the availabilities per country by provider.
        :param tv_id: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["watch_providers"] % tv_id,
            key="results"
        )

    def rate_tv_show(self, tv_id, rating):
        """
        Rate a TV show.
        :param tv_id: int
        :param rating: float
        """
        self._request_obj(
            self._urls_tv["rate_tv_show"] % tv_id,
            params="session_id=%s" % self.session_id,
            method="POST",
            json={"value": rating}
        )

    def delete_rating(self, tv_id):
        """
        Remove your rating for a TV show.
        :param tv_id: int
        """
        self._request_obj(
            self._urls_tv["delete_rating"] % tv_id,
            params="session_id=%s" % self.session_id,
            method="DELETE"
        )

    def latest(self):
        """
        Get the most newly created TV show. This is a live response and will continuously change.
        :return:
        """
        return self._request_obj(self._urls_tv["latest"])

    def airing_today(self, page=1):
        """
        Get a list of TV shows that are airing today.
        This query is purely day based as we do not currently support airing times.
        :param page: int
        :return:
        """
        return self._request_obj(
            self._urls_tv["airing_today"],
            params="page=%s" % page,
            key="results"
        )

    def on_the_air(self, page=1):
        """
        Get a list of shows that are currently on the air.
        :param page:
        :return:
        """
        return self._request_obj(
            self._urls_tv["on_the_air"],
            params="page=%s" % page,
            key="results"
        )

    def popular(self, page=1):
        """
        Get a list of the current popular TV shows on TMDb. This list updates daily.
        :param page:
        :return:
        """
        return self._request_obj(
            self._urls_tv["popular"],
            params="page=%s" % page,
            key="results"
        )

    def top_rated(self, page=1):
        """
        Get a list of the top rated TV shows on TMDb.
        :param page:
        :return:
        """
        return self._request_obj(
            self._urls_tv["top_rated"],
            params="page=%s" % page,
            key="results"
        )

    def get_tv_infos(self, term, page=1):
        """
        Search for a TV show.
        :param term:
        :param page:
        :return:
        """
        return Search().tv_shows(term, page=page)