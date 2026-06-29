# --- imports
from PySide6.QtCore import QObject, Signal

# shell level sector
class LowLevelBus(QObject):

    quitRequested = Signal()

mainBus = LowLevelBus()