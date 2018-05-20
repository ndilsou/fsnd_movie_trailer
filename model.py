"""
API to fetch external data.
"""

import requests
import media


class TheMovieDBApiFinder:
    """
    Finds a media's information on themoviedb.com.
    """

    SEARCH_URL = 'https://api.themoviedb.org/3/search/{media_type}'
    MEDIA_URL_TEMPLATE = "https://api.themoviedb.org/3/{media_type}/{media_id}"
    API_KEY = "14d3091648ed57efcf7c718f68ef77d5"  # API Key to TMDB.com.

    @property
    def media_type(self):
        """Media Type of the search. ex movie, tv, etc"""
        raise NotImplementedError()

    def find(self, search_query):
        """
        Search the API for the media.
        :return:
        """
        media_id = self.get_media_id(search_query)
        details = self.get_media_details(media_id)
        return self.create_media_from_details(details)

    def create_media_from_details(self, details):
        raise NotImplementedError()

    def get_media_id(self, search_query):
        """
        Search TheMovieDB for the media, returns the id of the first result.
        throws KeyError if the media could not be found or status code != 200.
        throws ValueError if status code != 200
        :param search_query: Details of the search query, such as media name, year or any other filter for the search.
        :return: str, id of the media.
        """
        url = self.SEARCH_URL.format(media_type=self.media_type)
        payload = dict(api_key=self.API_KEY, include_adult=False, **search_query)
        response = requests.get(url, payload)

        if response.status_code == 200:
            results = response.json()
            if results["total_results"] == 0:
                raise self._media_not_found(search_query, response.text)
            else:
                details = results["results"][0]
                media_id = details["id"]
        else:
            raise self._media_not_found(search_query, response.text)

        return media_id

    def get_media_details(self, media_id):
        """
        Queries TMDB.com for the details of the media, including videos and images.
        :param media_id:
        :return:
        """
        url = self.MEDIA_URL_TEMPLATE.format(media_type=self.media_type, media_id=media_id)
        payload = {
            "api_key": self.API_KEY,
            "append_to_response": "videos,images",
            "language": "en"
        }

        response = requests.get(url, payload)
        details = response.json()
        return details

    def _media_not_found(self, search_query, results):
        """
        Generates a KeyError indicating that the search failed.
        :return:
        """
        return KeyError(f"No {self.media_type} with details {search_query} was found.\n{results}")


class MovieFinder(TheMovieDBApiFinder):
    """
    Finds a movie's information on themoviedb.com.
    """

    @property
    def media_type(self):
        return "movie"

    def create_media_from_details(self, details):
        """
        Extracts the relevant details of the Movie from its raw form into a domain object for the application.
        :return: Movie
        """
        title = details["title"]
        plotline = details["overview"]
        youtube_trailer_url = self.first_youtube_trailer_url(details["videos"]["results"])
        poster_image_url = self.highest_voted_image(details["images"]["posters"])
        return media.Movie(title, plotline, poster_image_url, youtube_trailer_url)

    @staticmethod
    def first_youtube_trailer_url(videos):
        youtube_trailers = [video for video in videos if video["site"] == "YouTube" and video["type"] == "Trailer"]
        try:
            video = youtube_trailers[0]
        except IndexError:
            print("No Youtube Trailer available. Using first Youtube Video instead")
            youtube_videos = [video for video in videos if video["site"] == "YouTube"]
            try:
                video = youtube_videos[0]
            except IndexError:
                print("No youtube video available.")
                video = {"key": "XXXXXXXX"}

        youtube_trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
        return youtube_trailer_url

    @staticmethod
    def highest_voted_image(images):
        highest_vote = -1
        highest_voted_image = {"file_path": "/"}
        for image in images:
            if image["vote_average"] > highest_vote:
                highest_vote = image["vote_average"]
                highest_voted_image = image

        poster_image_url = f"https://image.tmdb.org/t/p/original{highest_voted_image['file_path']}"
        return poster_image_url


def get_finder_for_media_type(media_type):
    """
    Returns the appropriate finder class for the given media type
    :param media_type: 
    :return: 
    """
    finders = {
        "movie": MovieFinder
    }

    return finders[media_type]()


def load_media_collection(media_type, search_queries):
    """
    Loads a list of media of a given type from an external API.
    :param media_type: str, Type of the media to be displayed, ex. movies
    :param search_queries: list[str], Names of the media to be loaded form the API.
    :return: list[Media]
    """

    finder = get_finder_for_media_type(media_type)
    results = []
    for search_query in search_queries:
        try:
            result = finder.find(search_query)
            print(result)
        except KeyError:
            print(f"Could not find media with details {search_query}")
        else:
            results.append(result)

    return results


def load_default_media_collection(media_type, media_names):
    """
    Creates a fixed list of movies.
    :param media_type: str, Type of the media to be displayed, ex. movies, tv_shows, etc..
    :param media_names: list[str], Names of the media to be loaded.
    :return: list[Movie]
    """
    toy_story = media.Movie("Toy Story", "A story of a boy and his toys that come to life", "http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg", "https://www.youtube.com/watch2v=vwy3H85NOG4")
    school_of_rock = media.Movie("School of Rock", "Storyline", "http://upload.wikimedia.org/wikipedia/en/1/11/School_of_Rock_Poster.jpg", "https://www.youtube.com/watch2v=3PsUJFEBC74")
    ratatouille = media.Movie("Ratatouille", "Storyline", "http://upload.wikimedia.org/wikipedia/en/5/50/RatatouillePoster.jpg", "https://www.youtube.com/watch2v=c3sBBRxDAgk")
    midnight_in_paris = media.Movie("Midnight in Paris", "Storyline", "http://upload.wikimedia.org/wikipedia/en/9/9f/Midnight_in_Paris_Poster.jpg", "https://www.youtube.com/watch2v=atLg2wQ12mvu")
    hunger_games = media.Movie("Honger Games", "Storyline", "http://upload.wikimedia.org/wikipedia/en/4/42/HungerGamesPoster.jpg", "https://www.youtube.com/watch2v=PbA63a7H0bo")

    movies = [toy_story, school_of_rock, ratatouille, midnight_in_paris, hunger_games]
    return movies
