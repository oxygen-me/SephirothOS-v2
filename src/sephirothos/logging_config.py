"""SephirothOS logging configuration."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from sephirothos.paths import log_directory

LOGGER_NAME = "sephirothos"
LOG_FILENAME = "sephirothos.log"

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def configure_logging(
    directory: Path | None = None,
    *,
    verbose: bool = False,
    console: bool = True,
) -> Path:
    """Configure application logging and return the active log path."""

    target_directory = directory or log_directory()
    target_directory.mkdir(parents=True, exist_ok=True)

    log_path = target_directory / LOG_FILENAME
    level = logging.DEBUG if verbose else logging.INFO

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.propagate = False

    # Prevent duplicate handlers if initialization is repeated in tests
    # or during development.
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=2 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console and sys.stderr is not None:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logging.captureWarnings(True)

    return log_path
