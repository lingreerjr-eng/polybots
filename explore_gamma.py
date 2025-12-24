import requests
import json

def explore_gamma():
    url = "https://gamma-api.polymarket.com/markets"
    params = {
        "limit": 5,
        "active": "true",
        "closed": "false",
        "tag_slug": "crypto" # Checking crypto markets suitable for arb
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    explore_gamma()
