# --- imports
from PySide6.QtCore import QObject, Signal

# --- create bus
class EventBus(QObject):

    # --- system
    quitRequested = Signal()
    restartRequested = Signal()

    # --- ux
    clockUpdated = Signal(object)

mainBus = EventBus()