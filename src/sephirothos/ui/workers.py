"""Background Qt workers for blocking application services."""

from __future__ import annotations

from PySide6.QtCore import QObject, QRunnable, Signal

from sephirothos.services.announcements import (
    AnnouncementLoadError,
    AnnouncementService,
)


class AnnouncementWorkerSignals(QObject):
    """Signals emitted by an announcement-loading worker."""

    loaded = Signal(object)
    failed = Signal(str)
    finished = Signal()


class AnnouncementWorker(QRunnable):
    """Load announcements without blocking the Qt GUI thread."""

    def __init__(
        self,
        service: AnnouncementService,
    ) -> None:
        super().__init__()

        self._service = service
        self.signals = AnnouncementWorkerSignals()

    def run(self) -> None:
        try:
            feed = self._service.load()
        except AnnouncementLoadError as error:
            self.signals.failed.emit(str(error))
        else:
            self.signals.loaded.emit(feed)
        finally:
            self.signals.finished.emit()
