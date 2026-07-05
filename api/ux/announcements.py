import requests

ANNOUNCEMENTS_URL = "https://raw.githubusercontent.com/YOURNAME/YOURREPO/main/announcements.json"

def fetch_announcements():
    try:
        response = requests.get(ANNOUNCEMENTS_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[announcements]: fetch failed: {e}")
        return []