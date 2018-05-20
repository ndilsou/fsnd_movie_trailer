"""
Domain Objects representing the video content that can be displayed in the application.
"""


class Movie:
    """
    Represents a Movie.
    """

    def __init__(self, title, plotline, poster_image_url, trailer_youtube_url):
        self.title = title
        self.plotline = plotline
        self.trailer_youtube_url = trailer_youtube_url
        self.poster_image_url = poster_image_url

    def __repr__(self):
        return f"Movie({self.title}, {self.plotline[:30] + '...'}, {self.poster_image_url}, {self.trailer_youtube_url})"
