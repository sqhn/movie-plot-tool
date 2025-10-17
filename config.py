import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    OPENSUBTITLES_USERNAME = os.getenv('OPENSUBTITLES_USERNAME')
    OPENSUBTITLES_PASSWORD = os.getenv('OPENSUBTITLES_PASSWORD')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    @classmethod
    def validate(cls):
        missing = []
        if not cls.TMDB_API_KEY:
            missing.append('TMDB_API_KEY')
        if not cls.OPENSUBTITLES_USERNAME:
            missing.append('OPENSUBTITLES_USERNAME')
        if not cls.OPENSUBTITLES_PASSWORD:
            missing.append('OPENSUBTITLES_PASSWORD')
        if not cls.ANTHROPIC_API_KEY:
            missing.append('ANTHROPIC_API_KEY')
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")