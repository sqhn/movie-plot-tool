import os
import requests
from xmlrpc.client import ServerProxy

class OpenSubtitlesClient:
    def __init__(self, username=None, password=None):
        self.username = username or os.getenv('OPENSUBTITLES_USERNAME')
        self.password = password or os.getenv('OPENSUBTITLES_PASSWORD')
        self.server = ServerProxy('https://api.opensubtitles.org/xml-rpc')

    def search_subtitles(self, movie_title, language='en'):
        # Login to get token
        login_response = self.server.LogIn(self.username, self.password, 'en', 'TemporaryUserAgent')
        token = login_response['token']

        # Search for subtitles
        search_params = {
            'sublanguageid': language,
            'query': movie_title
        }
        results = self.server.SearchSubtitles(token, [search_params])

        if results['data']:
            return results['data'][0]  # Return the first result
        return None

    def download_subtitle(self, subtitle_id, output_path='subtitle.srt'):
        # Login to get token
        login_response = self.server.LogIn(self.username, self.password, 'en', 'TemporaryUserAgent')
        token = login_response['token']

        # Download subtitle
        download_response = self.server.DownloadSubtitles(token, [subtitle_id])
        if download_response['data']:
            subtitle_data = download_response['data'][0]
            subtitle_url = subtitle_data['data']

            # Decode base64 and save
            import base64
            import gzip
            subtitle_content = base64.b64decode(subtitle_url)

            # Check if it's gzipped
            if subtitle_content.startswith(b'\x1f\x8b'):
                subtitle_content = gzip.decompress(subtitle_content)

            with open(output_path, 'wb') as f:
                f.write(subtitle_content)
            return output_path
        return None