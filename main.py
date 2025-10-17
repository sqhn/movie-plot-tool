import sys
import os
from tmdb_client import TMDBClient
from opensubtitles_client import OpenSubtitlesClient
from claude_client import ClaudeClient
from config import Config

def get_movie_plot(movie_title):
    try:
        # Validate configuration
        Config.validate()

        # Initialize clients
        tmdb = TMDBClient()
        subtitles = OpenSubtitlesClient()
        claude = ClaudeClient()

        # Search for movie on TMDB
        movie = tmdb.search_movie(movie_title)
        if not movie:
            return "Movie not found on TMDB."

        # Get movie details
        details = tmdb.get_movie_details(movie.id)
        overview = details.overview

        # Search and download subtitles
        subtitle_result = subtitles.search_subtitles(movie_title)
        if not subtitle_result:
            return f"Plot summary from TMDB: {overview}\n\nNo subtitles found."

        subtitle_path = subtitles.download_subtitle(subtitle_result['IDSubtitleFile'])

        # Read subtitle text
        try:
            with open(subtitle_path, 'r', encoding='utf-8') as f:
                subtitle_text = f.read()
        except UnicodeDecodeError:
            # Try with latin-1 encoding if utf-8 fails
            with open(subtitle_path, 'r', encoding='latin-1') as f:
                subtitle_text = f.read()

        # Generate summary using Claude
        summary = claude.summarize_plot(overview, subtitle_text)

        # Clean up
        os.remove(subtitle_path)

        return summary
    except Exception as e:
        return f"Error retrieving movie plot: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py 'Movie Title'")
        sys.exit(1)

    movie_title = sys.argv[1]
    plot = get_movie_plot(movie_title)
    print(plot)