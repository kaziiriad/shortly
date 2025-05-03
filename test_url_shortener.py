import requests
import json

# Base URL of your application
BASE_URL = "http://localhost:8000"  # Change this if your app is running on a different URL

def create_short_url(original_url):
    """Create a short URL for the given original URL."""
    response = requests.post(f"{BASE_URL}/urls/create", params={"original_url": original_url})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error creating short URL: {response.status_code}")
        print(response.text)
        return None

def get_original_url(short_url_id):
    """Get the original URL for the given short URL ID."""
    response = requests.get(f"{BASE_URL}/urls/{short_url_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving original URL: {response.status_code}")
        print(response.text)
        return None

def main():
    # Create a short URL
    original_url = "https://www.example.com"
    print(f"Creating short URL for: {original_url}")
    
    result = create_short_url(original_url)
    if result:
        print(f"Short URL created: {result['short_url']}")
        print(f"Short URL ID: {result['short_url'].split('/')[-1]}")
        
        # Get the short URL ID from the result
        short_url_id = result['short_url'].split('/')[-1]
        
        # Retrieve the original URL
        print(f"\nRetrieving original URL for short URL ID: {short_url_id}")
        original = get_original_url(short_url_id)
        
        if original:
            print(f"Original URL: {original['original_url']}")
            print(f"Visit count: {original['visits']}")
        
if __name__ == "__main__":
    main()