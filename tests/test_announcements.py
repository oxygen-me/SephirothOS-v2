import json
from pathlib import Path

import pytest

from sephirothos.services.announcements import (
    AnnouncementLoadError,
    AnnouncementService,
    AnnouncementSource,
    AnnouncementValidationError,
)


def announcement(
    identifier: str,
    *,
    published_at: str = "2026-07-13T12:00:00Z",
    enabled: bool = True,
    minimum_version: str | None = None,
    maximum_version: str | None = None,
    action_url: str | None = None,
) -> dict[str, object]:
    return {
        "id": identifier,
        "title": f"Title for {identifier}",
        "body": f"Body for {identifier}",
        "published_at": published_at,
        "enabled": enabled,
        "minimum_version": minimum_version,
        "maximum_version": maximum_version,
        "action_url": action_url,
    }


def feed(
    *announcements: dict[str, object],
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "announcements": list(announcements),
    }


def make_service(
    tmp_path: Path,
    payload: object,
    *,
    current_version: str = "0.1.0a1",
) -> AnnouncementService:
    return AnnouncementService(
        current_version=current_version,
        cache_path=tmp_path / "announcements.json",
        fetch_announcements=lambda: payload,
    )


def test_valid_remote_feed_is_sorted_and_cached(
    tmp_path,
) -> None:
    payload = feed(
        announcement(
            "older",
            published_at="2026-07-12T12:00:00Z",
        ),
        announcement(
            "newer",
            published_at="2026-07-13T12:00:00Z",
        ),
    )
    service = make_service(tmp_path, payload)

    result = service.load()

    assert result.source is AnnouncementSource.REMOTE
    assert [item.identifier for item in result.announcements] == [
        "newer",
        "older",
    ]

    cached_payload = json.loads(
        (tmp_path / "announcements.json").read_text(
            encoding="utf-8",
        )
    )
    assert cached_payload == payload


def test_disabled_and_incompatible_announcements_are_excluded(
    tmp_path,
) -> None:
    payload = feed(
        announcement(
            "visible",
            minimum_version="0.1.0a1",
        ),
        announcement(
            "disabled",
            enabled=False,
        ),
        announcement(
            "too-new",
            minimum_version="0.2.0",
        ),
        announcement(
            "too-old",
            maximum_version="0.1.0a0",
        ),
    )
    service = make_service(tmp_path, payload)

    result = service.load()

    assert [item.identifier for item in result.announcements] == ["visible"]


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("published_at", "not-a-date"),
        ("published_at", "2026-07-13T12:00:00"),
        ("action_url", "http://example.com"),
        ("action_url", "not-a-url"),
    ],
)
def test_invalid_announcement_values_are_rejected(
    tmp_path,
    field_name,
    value,
) -> None:
    item = announcement("broken")
    item[field_name] = value

    service = make_service(
        tmp_path,
        feed(item),
    )

    with pytest.raises(AnnouncementLoadError) as captured:
        service.load()

    assert isinstance(
        captured.value.__cause__,
        AnnouncementValidationError,
    )


def test_duplicate_identifiers_are_rejected(
    tmp_path,
) -> None:
    service = make_service(
        tmp_path,
        feed(
            announcement("duplicate"),
            announcement("duplicate"),
        ),
    )

    with pytest.raises(AnnouncementLoadError) as captured:
        service.load()

    assert isinstance(
        captured.value.__cause__,
        AnnouncementValidationError,
    )


def test_remote_failure_uses_valid_cache(
    tmp_path,
) -> None:
    cache_path = tmp_path / "announcements.json"
    cache_path.write_text(
        json.dumps(
            feed(
                announcement("cached"),
            )
        ),
        encoding="utf-8",
    )

    def fail_fetch() -> object:
        raise OSError("Network unavailable")

    service = AnnouncementService(
        current_version="0.1.0a1",
        cache_path=cache_path,
        fetch_announcements=fail_fetch,
    )

    result = service.load()

    assert result.source is AnnouncementSource.CACHE
    assert [item.identifier for item in result.announcements] == ["cached"]


def test_remote_and_cache_failure_raise_load_error(
    tmp_path,
) -> None:
    def fail_fetch() -> object:
        raise OSError("Network unavailable")

    service = AnnouncementService(
        current_version="0.1.0a1",
        cache_path=tmp_path / "missing.json",
        fetch_announcements=fail_fetch,
    )

    with pytest.raises(AnnouncementLoadError):
        service.load()
