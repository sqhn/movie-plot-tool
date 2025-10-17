import requests
import time

def test_web_interface():
    """Test the web interface by making a request to search for Inception"""

    # Start the Flask app in the background (assuming it's already running)
    # In a real test, you'd start the server programmatically

    # Wait a moment for the server to be ready
    time.sleep(2)

    # Test the search functionality
    url = 'http://localhost:5000/search'
    data = {'movie_title': 'Inception'}

    try:
        response = requests.post(url, data=data, timeout=30)
        response.raise_for_status()

        result = response.json()

        # Validate the response structure
        assert 'title' in result, "Response should contain 'title'"
        assert 'release_date' in result, "Response should contain 'release_date'"
        assert 'vote_average' in result, "Response should contain 'vote_average'"
        assert 'poster_url' in result, "Response should contain 'poster_url'"
        assert 'plot' in result, "Response should contain 'plot'"

        # Validate specific content for Inception
        assert 'Inception' in result['title'], f"Title should contain 'Inception', got: {result['title']}"
        assert result['release_date'] == '2010-07-15', f"Release date should be '2010-07-15', got: {result['release_date']}"
        assert result['poster_url'] is not None, "Poster URL should not be None"
        assert 'Synopsis:' in result['plot'], f"Plot should contain 'Synopsis:', got: {result['plot'][:100]}..."
        assert 'Timeline' in result['plot'], f"Plot should contain 'Timeline', got: {result['plot'][:200]}..."
        assert 'Conclusion:' in result['plot'], f"Plot should contain 'Conclusion:', got: {result['plot'][:300]}..."
        assert 'Meta Analysis:' in result['plot'], f"Plot should contain 'Meta Analysis:', got: {result['plot'][:400]}..."

        print("✅ Web interface test passed!")
        print(f"Movie: {result['title']}")
        print(f"Release Date: {result['release_date']}")
        print(f"Rating: {result['vote_average']}/10")
        print(f"Has Poster: {'Yes' if result['poster_url'] else 'No'}")
        print(f"Plot Analysis Length: {len(result['plot'])} characters")

        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except AssertionError as e:
        print(f"❌ Validation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    success = test_web_interface()
    exit(0 if success else 1)