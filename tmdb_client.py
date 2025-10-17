import os
from tmdbv3api import TMDb, Movie

class TMDBClient:
    def __init__(self, api_key=None):
        self.tmdb = TMDb()
        self.tmdb.api_key = api_key or os.getenv('TMDB_API_KEY')
        self.movie = Movie()

    def search_movie(self, title):
        results = self.movie.search(title)
        if results:
            return results[0]  # Return the first result
        return None

    def get_movie_details(self, movie_id):
        return self.movie.details(movie_id)