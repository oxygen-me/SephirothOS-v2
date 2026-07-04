from datetime import datetime, timedelta
import time

from PySide6.QtCore import QThread

from eventbus import mainBus


class ClockService(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = True

    def stop(self):
        self._running = False
        self.wait()

    def run(self):
        while self._running:
            now = datetime.now()

            mainBus.clockUpdated.emit(now)

            next_second = (now + timedelta(seconds=1)).replace(microsecond=0)

            delay = (next_second - now).total_seconds()
            deadline = time.perf_counter() + delay

            while self._running:
                remaining = deadline - time.perf_counter()

                if remaining <= 0:
                    break

                if remaining > 0.005:
                    time.sleep(remaining - 0.001)