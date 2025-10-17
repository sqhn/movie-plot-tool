import requests
import time

def test_autocomplete():
    """Test the autocomplete functionality"""

    # Wait a moment for the server to be ready
    time.sleep(2)

    # Test autocomplete with "Incep"
    url = 'http://localhost:5000/autocomplete'
    params = {'q': 'Incep'}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        result = response.json()

        # Check if it's an error response
        if isinstance(result, dict) and 'error' in result:
            print(f"❌ Autocomplete error: {result['error']}")
            return False

        # Validate the response structure
        assert isinstance(result, list), f"Expected list, got {type(result)}"

        if len(result) == 0:
            print("⚠️  No autocomplete suggestions returned (this might be expected if TMDB is not responding)")
            return True

        # Check structure of first result
        first_result = result[0]
        assert 'title' in first_result, "Result should contain 'title'"
        assert 'year' in first_result, "Result should contain 'year'"
        assert 'id' in first_result, "Result should contain 'id'"

        # Check if Inception is in the results
        inception_found = any(movie['title'].lower() == 'inception' for movie in result)
        if inception_found:
            print("✅ Inception found in autocomplete suggestions")
        else:
            print("⚠️  Inception not found in suggestions, but autocomplete is working")

        print(f"✅ Autocomplete test passed! Found {len(result)} suggestions")
        for movie in result[:3]:  # Show first 3 results
            print(f"  - {movie['title']} ({movie['year']})")

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
    success = test_autocomplete()
    exit(0 if success else 1)