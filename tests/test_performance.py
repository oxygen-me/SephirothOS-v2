from random import Random
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import sephirothos.services.performance as performance_module
from sephirothos.services.performance import (
    PerformanceError,
    PerformanceService,
)


def install_mock_counter(
    monkeypatch,
    percentage: float = 30.0,
) -> Mock:
    """Prevent unit tests from opening a real Windows PDH query."""

    counter = Mock()
    counter.value.return_value = percentage

    monkeypatch.setattr(
        performance_module,
        "WinCounter",
        lambda _path: counter,
    )

    return counter


def test_performance_snapshot_uses_system_metrics(
    monkeypatch,
) -> None:
    cpu_values = iter([0.0, 42.5])

    monkeypatch.setattr(
        performance_module.psutil,
        "cpu_percent",
        lambda interval=None: next(cpu_values),
    )
    monkeypatch.setattr(
        performance_module.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(percent=37.5),
    )

    install_mock_counter(
        monkeypatch,
        percentage=30.0,
    )

    service = PerformanceService(
        randomizer=Random(1),
    )
    snapshot = service.snapshot()

    assert snapshot.cpu_percentage == pytest.approx(42.5)
    assert snapshot.memory_percentage == pytest.approx(37.5)
    assert snapshot.disk_activity_percentage == pytest.approx(30.0)
    assert 0 <= snapshot.piss_percentage <= 100


def test_performance_percentages_are_clamped(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        performance_module.psutil,
        "cpu_percent",
        lambda interval=None: 150.0,
    )
    monkeypatch.setattr(
        performance_module.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(percent=-10.0),
    )

    install_mock_counter(
        monkeypatch,
        percentage=125.0,
    )

    service = PerformanceService()
    snapshot = service.snapshot()

    assert snapshot.cpu_percentage == 100.0
    assert snapshot.memory_percentage == 0.0
    assert snapshot.disk_activity_percentage == 100.0


def test_psutil_errors_are_wrapped(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        performance_module.psutil,
        "cpu_percent",
        lambda interval=None: 0.0,
    )

    install_mock_counter(monkeypatch)

    service = PerformanceService()

    def fail_memory_read():
        raise OSError("Performance counters unavailable")

    monkeypatch.setattr(
        performance_module.psutil,
        "virtual_memory",
        fail_memory_read,
    )

    with pytest.raises(PerformanceError):
        service.snapshot()


def test_disk_counter_errors_are_wrapped(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        performance_module.psutil,
        "cpu_percent",
        lambda interval=None: 0.0,
    )
    monkeypatch.setattr(
        performance_module.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(percent=50.0),
    )

    counter = install_mock_counter(monkeypatch)
    counter.value.side_effect = OSError("PDH counter unavailable")

    service = PerformanceService()

    with pytest.raises(PerformanceError):
        service.snapshot()


def test_close_releases_disk_counter(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        performance_module.psutil,
        "cpu_percent",
        lambda interval=None: 0.0,
    )

    counter = install_mock_counter(monkeypatch)
    service = PerformanceService()

    service.close()

    counter.close.assert_called_once_with()
