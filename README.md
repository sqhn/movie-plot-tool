# Movie Plot Tool

A tool to retrieve movie plot summaries using TMDB, OpenSubtitles, and Claude AI.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file based on `.env.example` and fill in your API keys:
   - TMDB API Key: Get from [TMDB](https://www.themoviedb.org/settings/api)
   - OpenSubtitles credentials: Sign up at [OpenSubtitles](https://www.opensubtitles.com/)
   - Anthropic API Key: Get from [Anthropic](https://console.anthropic.com/)

## Usage

Run the tool with a movie title:
```bash
python main.py "The Shawshank Redemption"
```

## How it works

1. Searches for the movie on TMDB to get basic information
2. Downloads subtitles from OpenSubtitles
3. Uses Claude AI to generate a plot summary combining TMDB overview and subtitle content