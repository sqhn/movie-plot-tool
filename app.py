from flask import Flask, render_template, request, jsonify
from tmdb_client import TMDBClient
from opensubtitles_client import OpenSubtitlesClient
from claude_client import ClaudeClient
from config import Config
import os

app = Flask(__name__)

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
            return {"error": "Movie not found on TMDB."}

        # Get movie details
        details = tmdb.get_movie_details(movie.id)
        overview = details.overview
        poster_path = details.poster_path
        title = details.title
        release_date = details.release_date
        vote_average = details.vote_average

        # Search and download subtitles
        subtitle_result = subtitles.search_subtitles(movie_title)
        if not subtitle_result:
            return {
                "title": title,
                "release_date": release_date,
                "vote_average": vote_average,
                "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
                "plot": f"Plot summary from TMDB: {overview}\n\nNo subtitles found."
            }

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

        return {
            "title": title,
            "release_date": release_date,
            "vote_average": vote_average,
            "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
            "plot": summary
        }
    except Exception as e:
        return {"error": f"Error retrieving movie plot: {str(e)}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    movie_title = request.form.get('movie_title')
    if not movie_title:
        return jsonify({"error": "Please enter a movie title."})

    result = get_movie_plot(movie_title)
    return jsonify(result)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '').strip()
    if not query or len(query) < 2:
        return jsonify([])

    try:
        Config.validate()
        tmdb = TMDBClient()

        # Search for movies matching the query
        results = tmdb.movie.search(query)

        # Format results for autocomplete
        suggestions = []
        for movie in results[:5]:  # Limit to 5 suggestions
            suggestions.append({
                'title': movie.title,
                'year': movie.release_date[:4] if movie.release_date else '',
                'id': movie.id
            })

        return jsonify(suggestions)

    except Exception as e:
        return jsonify({"error": f"Autocomplete failed: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)