"""
Domain Objects representing the video content that can be displayed in the application.
"""


class Movie:
    """
    Represents a Movie.
    """

    def __init__(self, title, description, poster_image_url, trailer_youtube_url):
        self.title = title
        self.description = description
        self.trailer_youtube_url = trailer_youtube_url
        self.poster_image_url = poster_image_url
