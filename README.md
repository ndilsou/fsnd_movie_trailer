# Movie Trailer Website

Static website to display movie trailers. Data is pulled from [The Movie DB](https://www.themoviedb.org/).
To add new movies, add entries to [media.json](./media.json) in the form:
  ```
      { 
        "query": <Movie Name>,
        "year": <Release Year>
      }
   ```
   
   For example to add Spirited Away:
   
   ```
       {
            "query": "Spirited Away",
            "year": "2002"
       }
```
***

## Installation

Dependencies: This application is built to work with Python 3.6+. 
In the following I assume that you have an installation for Python 3.6.
You can obtain one from the language [official website](https://www.python.org/downloads/)
or through [Anaconda](https://www.anaconda.com/download/).

1. Clone the repository.
2. Create your virtual environment running Python 3.6. example with virtualenv: `virtualenv movie_trailer_website -p 
<PATH_TO_PY36>`
3. Activate the environment and update pip. 
4. Install the requirements: `pip install -r requirements.txt`
5. Run the tests: `python -m unittest`
6. Run the app: `python app.py`
