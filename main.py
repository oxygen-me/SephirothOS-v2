import os
import sys
import json
import subprocess
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from bootstrap import Bootstrapper
from eventbus import mainBus
from gitfetch import GitFetch

from core.app import AppShell

from api.ux.clock import ClockService

viable_editions = ["[1] Basic", "[2] Workplace", "[3] Premium", "[4] Ultimate"]
lcn_path = Path(str(os.getenv('APPDATA'))) / 'SephirothOS' / 'license.json'
cfg_path = Path(str(os.getenv('APPDATA'))) / 'SephirothOS' / 'config.json'
VERSION = "pre-alpha-2"

print(f"[main]: Running version {VERSION}")
print(f"[main]: Running from: {sys.executable}")

# --- main function
def main():
    print("[main]: Start initiated")


    # --- create app
    app = QApplication(sys.argv)
    print("[main]: App created")

    # --- start clock
    print("[main]: Init clock")
    clock = ClockService()
    clock.start()

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
        print("[main]: Fetch failed. Notify user.")
        QMessageBox.warning(None,
                            "Hold up!",
                            "We were unable to fetch some data from GitHub. If there's a new version, you might not be able to install it. We don't care if you don't care. If you DO happen to care, check your internet or something. I don't fucking know.",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok)

    # --- bus user exit
    mainBus.quitRequested.connect(quit_app)
    mainBus.restartRequested.connect(restart_app)

    print(f"[main]: VERSION {VERSION!r}")
    print(f"[main]: osversion {osversion!r}")
    print(f"[main]: Equal {VERSION == osversion}")

    if VERSION != osversion:
        userchoice = QMessageBox.question(None, "Update Available", "I AM FUCKING RENDERING SOMETHING!!!",
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                          QMessageBox.StandardButton.Yes
                                          )

        if userchoice == QMessageBox.StandardButton.Yes:
            subprocess.Popen([
                "elevator.exe",
                "--pid",
                str(os.getpid())
            ])
            sys.exit(0)
        else:
            print("[main]: update declined")

    # --- create window depending on thing
    if lcn["edition"] not in viable_editions:
        raise PermissionError("Invalid edition. Do not tamper or pirate my shit.")

    if lcn["flag"] == "seth67":
        from core.welcome import WelcomeWindow
        intro = WelcomeWindow()
        intro.show()
    else:
        with open(cfg_path, "r", encoding="utf-8") as f:
            configdata = json.load(f)
        window = AppShell(cfgdata=configdata)
        window.show()

    exit_code = app.exec()

    # --- stop clock
    clock.stop()

    sys.exit(exit_code)

# --- restart function
def restart_app():
    print("[main]: Restarting app")
    os.execv(sys.executable, [sys.executable] + sys.argv)

def quit_app():
    print("[main]: Quitting app")
    QApplication.quit()

# --- run function
if __name__ == "__main__":
    main()