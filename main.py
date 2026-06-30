# --- imports
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from bootstrap import Bootstrapper
from eventbus import mainBus
from gitfetch import GITFetch

from core.app import AppShell

viable_editions = ["[1] Basic", "[2] Workplace", "[3] Premium", "[4] Ultimate"]

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

    # --- attempt fetch
    print("[main]: Attempting fetch...")

    fetcht = GITFetch()
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