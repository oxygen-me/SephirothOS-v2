# --- import json controller and Path
import json
from pathlib import Path
import os

# --- define requirements
required_keys =  ["edition", "flag"]
license_path = Path(str(os.getenv('APPDATA'))) / 'SephirothOS' / 'license.json'

# --- create bootstrapper class
class Bootstrapper:
    def __init__(self):
        self.ready = False
        self.data = {}

    # --- master bootstrap function
    def intitialize(self):
        print("[Bootstrapper]: Starting checks...")

        # --- attempt to fetch data
        try:
            self.data = self._load_lcn()
        except Exception as e:
            raise RuntimeError(e)

        # --- verify keys
        for key in required_keys:
            if key not in self.data:
                raise RuntimeError(f"[Bootstrapper]: Missing required key in license: {key}")

        # --- debug completion and return params to main.py
        print("[Bootstrapper]: Checks complete.")
        print(self.data)

        self.ready = True
        return self.ready, self.data

    # --- load and parse license.json
    def _load_lcn(self):
        with open(license_path, "r") as f:
            lcn = json.load(f)
            return lcn