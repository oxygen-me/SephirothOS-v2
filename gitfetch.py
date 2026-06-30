import requests

class GITFetch:
    def __init__(self):
        self.osversion = ""
        self.success = False

    def version_fetch(self):
        url = f"https://api.github.com/repos/oxygen-me/SephirothOS-v2/releases/latest"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.osversion = data["tag_name"]
                print("[gitfetch]: " + self.osversion)

                self.success = True

                return self.success, self.osversion

            else:
                print(f"[gitfetch]: Unable to retrieve latest release (Status Code: {response.status_code})")
                self.success = False
                self.osversion = "ERR"
                return self.success, self.osversion
        except:
            print(f"[gitfetch]: Unable to retrieve latest release")
            self.success = False
            self.osversion = "ERR"
            return self.success, self.osversion