import os
from anthropic import Anthropic

class ClaudeClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key)

    def summarize_plot(self, tmdb_overview, subtitle_text):
        prompt = f"""
        Based on the following movie overview from TMDB and subtitle text, provide a comprehensive movie analysis with the following structure:

        TMDB Overview: {tmdb_overview}

        Subtitle Text (first 5000 characters): {subtitle_text[:5000]}

        Please structure your response as follows:

        **Synopsis:**
        [Brief overview of the movie's premise]

        **Timeline (5-10 key steps):**
        1. [Step 1]
        2. [Step 2]
        ...
        [Up to 10 steps]

        **Conclusion:**
        [How the story resolves]

        **Meta Analysis:**
        [Themes, symbolism, character development, or other deeper analysis]
        """
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text