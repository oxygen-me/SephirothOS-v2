# --- imports
from colorama import init, Fore, Style

# --- initialize colorama automatically after each print
init(autoreset=True)

# --- helper function
def _log(level: str, color: str, message: str, source: str):
    prefix = f"[{level}]".ljust(12)
    print(color + f"{prefix}[{source}]: {message}")

# --- callables
def info(message: str, source: str):
    _log("INFO", "", message, source)

def debug(message: str, source: str):
    _log("DEBUG", Fore.LIGHTBLACK_EX, message, source)

def success(message: str, source: str):
    _log("SUCCESS", Fore.LIGHTGREEN_EX, message, source)

def warning(message: str, source: str):
    _log("WARNING", Fore.YELLOW, message, source)

def error(message: str, source: str):
    _log("ERROR", Fore.RED, message, source)

def critical(message: str, source: str):
    _log("CRITICAL", Fore.LIGHTRED_EX + Style.BRIGHT, message, source)

def important(message: str, source: str):
    _log("IMPORTANT", Fore.LIGHTCYAN_EX + Style.BRIGHT, message, source)