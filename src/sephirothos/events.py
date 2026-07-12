"""Application-wide event signals."""

from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    """Signals for requests that cross application boundaries."""

    quit_requested = Signal()
    restart_requested = Signal()
    notification_requested = Signal(str)
