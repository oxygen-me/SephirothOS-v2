# --- imports
import os
import sys
import subprocess
import json
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from bootstrap import Bootstrapper
from eventbus import mainBus
from gitfetch import GitFetch

from core.app import AppShell

viable_editions = ["[1] Basic", "[2] Workplace", "[3] Premium", "[4] Ultimate"]
lcn_path = Path(str(os.getenv('APPDATA'))) / 'SephirothOS' / 'license.json'
VERSION = "0.2.3"

print(f"[main]: Running version {VERSION}")
print(f"Running from: {sys.executable}")

# --- main function
def main():
    print("[main]: Start initiated")

    # --- create app
    app = QApplication(sys.argv)

    # --- attempt handshake
    print("[main]: Attempting handshake...")

    boot = Bootstrapper()
    ready, lcn = boot.intitialize()

    # --- parse return
    if not ready:
        raise RuntimeError("[main] Bootstrap failed!")

    print("[main]: Handshake finalized")

    # --- check update flag at root level
    with open(lcn_path)  as f:
        data = json.load(f)

        if data.get("upd"):

            print("[main]: Detected ongoing update")
            print("[main]: Cleaning up...")

            if os.path.exists("elevator.new.exe"):
                try:
                    os.remove("elevator.exe")
                except FileNotFoundError:
                    pass

                os.replace("elevator.new.exe", "elevator.exe")

            data["upd"] = False

            with open(lcn_path, "w")  as f:
                json.dump(data, f, indent=4)

    # --- attempt fetch
    print("[main]: Attempting fetch...")

    fetcht = GitFetch()
    success, osversion = fetcht.version_fetch()

    # --- parse return
    if not success:
        QMessageBox.warning(None,
                            "Hold up!",
                            "We were unable to fetch some data from GitHub. If there's a new version, you might not be able to install it. We don't care if you don't care. If you DO happen to care, check your internet or something. I don't fucking know.",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)

    # --- bus user exit
    mainBus.quitRequested.connect(app.quit)

    print("=" * 50)
    print(f"VERSION   : {VERSION!r}")
    print(f"osversion : {osversion!r}")
    print(f"Equal?    : {VERSION == osversion}")
    print("=" * 50)

    if VERSION != osversion:
        subprocess.Popen([
            "elevator.exe",
            "--pid",
            str(os.getpid())
        ])

        sys.exit(0)

    # --- create window depending on thing
    if lcn["edition"] not in viable_editions:
        raise PermissionError("Invalid edition. Do not tamper or pirate my shit.")

    if lcn["flag"] == "seth67":
        from core.welcome import WelcomeWindow
        intro = WelcomeWindow(lcn=lcn)
        intro.show()
    else:
        window = AppShell() # todo: add config JSON stuff later
        window.show()

    sys.exit(app.exec())

# --- run function
if __name__ == "__main__":
    main()