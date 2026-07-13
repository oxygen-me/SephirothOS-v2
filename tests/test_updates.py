import pytest

from sephirothos.services.updates import (
    UpdateCheckError,
    UpdateService,
)


def release(
    tag: str,
    *,
    prerelease: bool = False,
    draft: bool = False,
) -> dict[str, object]:
    return {
        "tag_name": tag,
        "name": tag,
        "html_url": f"https://example.test/{tag}",
        "body": "Release notes",
        "prerelease": prerelease,
        "draft": draft,
    }


def test_newer_alpha_release_is_available() -> None:
    service = UpdateService(
        current_version="0.1.0a1",
        release_channel="alpha",
        fetch_releases=lambda: [
            release("0.1.0a2", prerelease=True),
        ],
    )

    result = service.check()

    assert result.update_available is True
    assert result.latest_release is not None
    assert result.latest_release.tag == "0.1.0a2"


def test_current_release_is_not_an_update() -> None:
    service = UpdateService(
        current_version="0.1.0a1",
        release_channel="alpha",
        fetch_releases=lambda: [
            release("0.1.0a1", prerelease=True),
        ],
    )

    assert service.check().update_available is False


def test_older_release_is_not_an_update() -> None:
    service = UpdateService(
        current_version="0.2.0",
        release_channel="alpha",
        fetch_releases=lambda: [
            release("0.1.0"),
        ],
    )

    assert service.check().update_available is False


def test_v_prefix_is_accepted() -> None:
    service = UpdateService(
        current_version="0.1.0",
        release_channel="stable",
        fetch_releases=lambda: [
            release("v0.2.0"),
        ],
    )

    result = service.check()

    assert result.latest_release is not None
    assert str(result.latest_release.version) == "0.2.0"


def test_stable_channel_ignores_prereleases() -> None:
    service = UpdateService(
        current_version="0.1.0",
        release_channel="stable",
        fetch_releases=lambda: [
            release("0.2.0a1", prerelease=True),
            release("0.1.1"),
        ],
    )

    result = service.check()

    assert result.latest_release is not None
    assert result.latest_release.tag == "0.1.1"


def test_drafts_and_invalid_tags_are_ignored() -> None:
    service = UpdateService(
        current_version="0.1.0",
        release_channel="alpha",
        fetch_releases=lambda: [
            release("0.3.0", draft=True),
            release("alpha-nightly-whatever"),
            release("0.2.0"),
        ],
    )

    result = service.check()

    assert result.latest_release is not None
    assert result.latest_release.tag == "0.2.0"


def test_invalid_response_raises_update_error() -> None:
    service = UpdateService(
        fetch_releases=lambda: {"message": "rate limited"},
    )

    with pytest.raises(UpdateCheckError):
        service.check()
