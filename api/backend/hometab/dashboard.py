# --- imports

from dataclasses import dataclass
import socket
import psutil
import time

import win32pdh

from utils.config import VERSION

from PySide6.QtCore import QObject, Signal, Slot, QTimer

@dataclass
class Performance:
    cpu: float
    ram: float
    disk_active: float
    net_up: int
    net_down: int

@dataclass
class Storage:
    path: str
    total: int
    used: int
    free: int
    percent: float
    total_text: str
    used_text: str
    free_text: str

@dataclass
class DashboardSnapshot:
    system_name: str
    os_name: str
    uptime: str
    performance: Performance
    storage: Storage
    status: list[str]

def format_uptime(seconds: float) -> str:
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)

    if days:
        return f"{days}d {hours}h {minutes}m"
    return f"{hours}h {minutes}m"

def format_bytes(num: int | float) -> str:
    units = ["B", "KB", "MB", "GB", "TB", "PB"]

    size = float(num)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024

def get_dashboard_snapshot(disk_active: float = 0.0) -> DashboardSnapshot:
    disk = psutil.disk_usage("/")
    mem = psutil.virtual_memory()
    net = psutil.net_io_counters()

    uptime = time.time() - psutil.boot_time()

    return DashboardSnapshot(
        system_name=socket.gethostname(),
        os_name=f"Sephiroth OS {VERSION}",
        uptime=format_uptime(uptime),
        performance=Performance(
            cpu=psutil.cpu_percent(interval=None),
            ram=mem.percent,
            disk_active=disk_active,
            net_up=net.bytes_sent,
            net_down=net.bytes_recv,
        ),
        storage=Storage(
            path="/",
            total=disk.total,
            used=disk.used,
            free=disk.free,
            percent=disk.percent,
            total_text=format_bytes(disk.total),
            used_text=format_bytes(disk.used),
            free_text=format_bytes(disk.free),
        ),
        status=[
            "Running",
            "Chud-Like in Nature",
            "Mining Bitcoin"
        ]
    )

class DashboardBackend(QObject):
    updated = Signal(object)

    def __init__(self, interval_ms=1000):
        super().__init__()
        self.interval_ms = interval_ms
        self.timer = None
        self.prev_disk = None
        self.prev_time = None
        self.disk_counter = WinCounter(r"\PhysicalDisk(_Total)\% Disk Time")

    @Slot()
    def start(self):
        psutil.cpu_percent(interval=None)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(self.interval_ms)

        self.update()

    @Slot()
    def update(self):
        disk_active = self.get_disk_active_percent()
        snapshot = get_dashboard_snapshot(disk_active)
        self.updated.emit(snapshot)

    def get_disk_active_percent(self) -> float:
        try:
            value = self.disk_counter.value()
            return max(0.0, min(100.0, value))
        except Exception:
            return 0.0

class WinCounter:
    def __init__(self, path: str):
        self.query = win32pdh.OpenQuery()
        self.counter = win32pdh.AddCounter(self.query, path)
        win32pdh.CollectQueryData(self.query)

    def value(self) -> float:
        win32pdh.CollectQueryData(self.query)
        _, val = win32pdh.GetFormattedCounterValue(
            self.counter,
            win32pdh.PDH_FMT_DOUBLE
        )
        return float(val)