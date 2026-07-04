# --- imports
import requests

# --- create MKPFetch class
class MKPFetch:
    def __init__(self, repo: str):
        self.repo = repo
        self.base = f"https://api.github.com/repos/{repo}"

    def get_repo_info(self):
        r = requests.get(self.base)
        r.raise_for_status()
        data = r.json()

        return {
            "name": data.get("name"),
            "full_name": data.get("full_name"),
            "description": data.get("description"),
            "author_name": data.get["owner"]["login"],
            "stars": data.get("stargazers_count"),
            "url": data.get("html_url"),
        }

    def get_readme(self):
        url = self.base + "/readme"
        r = requests.get(url, headers={"Accept": "application/vnd.github.v3.raw"})
        r.raise_for_status()
        return r.text

    def get_latest_release(self):
        url = self.base + "/releases/latest"
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        return{
            "tag": data.get("tag_name"),
            "name": data.get("name"),
            "body": data.get("body"),
            "assets": [
                {
                    "name": a["name"],
                    "url": a["browser_download_url"],
                }
                for a in data.get("assets", [])
            ]
        }