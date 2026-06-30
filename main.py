# --- imports
import sys
from PySide6.QtWidgets import QApplication
import json
from bootstrap import Bootstrapper
from eventbus import mainBus

from core.app import AppShell

viable_editions = ["[1] Basic", "[2] Workplace", "[3] Premium", "[4] Ultimate"]

# --- main function
def main():
    print("[Main]: Start initiated")

    # --- create app
    app = QApplication(sys.argv)

    # --- attempt handshake
    print("[Main]: Attempting handshake...")

    boot = Bootstrapper()
    ready, lcn = boot.intitialize()

    # --- parse return
    if not ready:
        raise RuntimeError("[Main] Bootstrap failed!")

    print("[Main]: Handshake finalized")

    # --- bus user exit
    mainBus.quitRequested.connect(app.quit)

    # --- create window depending on thing
    if lcn["edition"] not in viable_editions:
        raise PermissionError("Edition invalid!")

    if lcn["flag"] == "seth67":
        from core.welcome import WelcomeWindow
        intro = WelcomeWindow(lcn=lcn)
        intro.show()
    else:
        window = AppShell(lcn=lcn) # todo: add config later
        window.show()

    sys.exit(app.exec())

# --- run function
if __name__ == "__main__":
    main()