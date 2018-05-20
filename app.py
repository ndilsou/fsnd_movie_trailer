import json
import model
from fresh_tomatoes import open_movies_page

DEBUG = False


def main(load_media_collection_functor):
    """
    Entry point into the application. Fetch the collection of movies to display and displays the page.
    :arg load_media_collection_functor functor of signature f(media_type, media_names) used to fetch the Movies object.
    :return: None
    """
    with open("./media.json", "rt") as fh:
        available_media = json.load(fh)

    media = []
    for media_type, media_names in available_media.items():
        media.extend(load_media_collection_functor(media_type, media_names))

    open_movies_page(media)


if __name__ == '__main__':
    if DEBUG:
        load_media_functor = model.load_default_media_collection
    else:
        load_media_functor = model.load_media_collection

    main(load_media_functor)
