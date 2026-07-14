from pathlib import Path
from types import SimpleNamespace

import pytest

import sephirothos.services.storage as storage_module
from sephirothos.services.storage import (
    StorageError,
    StorageService,
)


def test_storage_snapshot_contains_capacity_information(
    monkeypatch,
) -> None:
    def fake_disk_usage(_root):
        return SimpleNamespace(
            total=1000,
            used=250,
            free=750,
        )

    monkeypatch.setattr(
        storage_module,
        "disk_usage",
        fake_disk_usage,
    )

    service = StorageService(Path("C:\\"))
    snapshot = service.snapshot()

    assert snapshot.root == Path("C:\\")
    assert snapshot.total_bytes == 1000
    assert snapshot.used_bytes == 250
    assert snapshot.free_bytes == 750
    assert snapshot.used_percentage == pytest.approx(25.0)


def test_storage_errors_are_wrapped(
    monkeypatch,
) -> None:
    def failing_disk_usage(_root):
        raise OSError("Drive unavailable")

    monkeypatch.setattr(
        storage_module,
        "disk_usage",
        failing_disk_usage,
    )

    service = StorageService(Path("Z:\\"))

    with pytest.raises(StorageError):
        service.snapshot()
