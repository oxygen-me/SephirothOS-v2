# --- imports
import sys
from PySide6.QtWidgets import QApplication

from bootstrap import Bootstrapper
from eventbus import mainBus
from core.app import AppShell

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

    # --- create window
    window = AppShell(lcn=lcn) # todo: add config later
    window.show()

    sys.exit(app.exec())

# --- run function
if __name__ == "__main__":
    main()