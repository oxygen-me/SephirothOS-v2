from pathlib import Path
import tempfile
import zipfile
import shutil
import requests
import json
import os


class MKPInstaller:

    REQUIRED_FIELDS = {
        "id",
        "name",
        "version",
        "author",
        "description",
        "module",
    }

    def __init__(self, progress_callback=None):
        self.progress = progress_callback or (lambda p, t: None)

        self.apps_dir = (
            Path(os.getenv("LOCALAPPDATA"))
            / "Sephiroth"
            / "common"
            / "apps"
        )

    def install(self, download_url: str):

        self.apps_dir.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory() as tmp:

            tmp = Path(tmp)

            zip_path = tmp / "app.zip"
            extract_path = tmp / "extract"

            self.progress(5, "Downloading app...")

            r = requests.get(download_url, stream=True)
            r.raise_for_status()

            total = int(r.headers.get("content-length", 0))
            downloaded = 0

            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(8192):

                    if not chunk:
                        continue

                    f.write(chunk)
                    downloaded += len(chunk)

                    if total:
                        self.progress(
                            5 + int(downloaded / total * 40),
                            "Downloading app..."
                        )

            self.progress(50, "Extracting...")

            with zipfile.ZipFile(zip_path) as z:
                z.extractall(extract_path)

            contents = list(extract_path.iterdir())

            if len(contents) == 1 and contents[0].is_dir():
                root = contents[0]
            else:
                root = extract_path

            manifest_path = root / "manifest.json"

            if not manifest_path.exists():
                raise RuntimeError("manifest.json not found.")

            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)

            missing = self.REQUIRED_FIELDS - manifest.keys()

            if missing:
                raise RuntimeError(
                    f"manifest.json missing fields: {', '.join(sorted(missing))}"
                )

            app_id = manifest["id"]

            install_dir = self.apps_dir / app_id

            self.progress(65, "Installing...")

            if install_dir.exists():
                shutil.rmtree(install_dir)

            shutil.copytree(root, install_dir)

            self.progress(100, "Installation complete.")

            return manifest