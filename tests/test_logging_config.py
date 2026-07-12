import logging

import pytest

from sephirothos.logging_config import (
    LOG_FILENAME,
    LOGGER_NAME,
    configure_logging,
)


@pytest.fixture(autouse=True)
def clean_application_logger():
    """Remove application handlers after every test."""

    yield

    logger = logging.getLogger(LOGGER_NAME)

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def flush_handlers() -> None:
    logger = logging.getLogger(LOGGER_NAME)

    for handler in logger.handlers:
        handler.flush()


def test_configure_logging_creates_log_file(tmp_path) -> None:
    log_path = configure_logging(
        tmp_path,
        console=False,
    )

    assert log_path == tmp_path / LOG_FILENAME
    assert log_path.exists()


def test_application_message_is_written_to_file(tmp_path) -> None:
    log_path = configure_logging(
        tmp_path,
        console=False,
    )

    logger = logging.getLogger("sephirothos.test")
    logger.info("Logging test message")

    flush_handlers()

    contents = log_path.read_text(encoding="utf-8")

    assert "Logging test message" in contents
    assert "sephirothos.test" in contents
    assert "INFO" in contents


def test_debug_messages_are_hidden_by_default(tmp_path) -> None:
    log_path = configure_logging(
        tmp_path,
        verbose=False,
        console=False,
    )

    logger = logging.getLogger("sephirothos.test")
    logger.debug("Hidden debug message")
    logger.info("Visible info message")

    flush_handlers()

    contents = log_path.read_text(encoding="utf-8")

    assert "Hidden debug message" not in contents
    assert "Visible info message" in contents


def test_verbose_logging_includes_debug_messages(tmp_path) -> None:
    log_path = configure_logging(
        tmp_path,
        verbose=True,
        console=False,
    )

    logger = logging.getLogger("sephirothos.test")
    logger.debug("Visible debug message")

    flush_handlers()

    contents = log_path.read_text(encoding="utf-8")

    assert "Visible debug message" in contents
    assert "DEBUG" in contents


def test_reconfiguration_does_not_duplicate_handlers(tmp_path) -> None:
    configure_logging(tmp_path, console=False)
    configure_logging(tmp_path, console=False)

    logger = logging.getLogger(LOGGER_NAME)

    assert len(logger.handlers) == 1
