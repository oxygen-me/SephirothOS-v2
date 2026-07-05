import platform
import psutil
import wmi


def bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 2)


def get_drives():
    drives = []

    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue

        drives.append({
            "device": part.device,              # C:\
            "mountpoint": part.mountpoint,
            "filesystem": part.fstype,
            "total_gb": bytes_to_gb(usage.total),
            "used_gb": bytes_to_gb(usage.used),
            "free_gb": bytes_to_gb(usage.free),
            "percent_used": usage.percent,
        })

    return drives


def get_ram():
    ram = psutil.virtual_memory()

    return {
        "total_gb": bytes_to_gb(ram.total),
        "used_gb": bytes_to_gb(ram.used),
        "available_gb": bytes_to_gb(ram.available),
        "percent_used": ram.percent,
    }


def get_cpu():
    c = wmi.WMI()
    cpu = c.Win32_Processor()[0]

    return {
        "model": cpu.Name.strip(),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "usage_percent": psutil.cpu_percent(interval=0.2),
        "architecture": platform.machine(),
    }


def get_gpu():
    c = wmi.WMI()
    gpus = []

    for gpu in c.Win32_VideoController():
        gpus.append({
            "name": gpu.Name,
            "driver_version": gpu.DriverVersion,
            "vram_gb": bytes_to_gb(int(gpu.AdapterRAM or 0)),
        })

    return gpus


def get_system_info():
    return {
        "os": platform.platform(),
        "drives": get_drives(),
        "ram": get_ram(),
        "cpu": get_cpu(),
        "gpu": get_gpu(),
    }