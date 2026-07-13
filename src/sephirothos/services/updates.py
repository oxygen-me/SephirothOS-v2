"""GitHub release discovery and version comparison."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from urllib.request import Request, urlopen

from packaging.version import InvalidVersion, Version

from sephirothos.metadata import RELEASE_CHANNEL, RELEASES_URL, VERSION

RELEASES_API_URL = "https://api.github.com/repos/oxygen-me/SephirothOS-v2/releases?per_page=30"

ReleaseFetcher = Callable[[], object]


class UpdateCheckError(RuntimeError):
    """Raised when release information cannot be retrieved or decoded."""


@dataclass(frozen=True, slots=True)
class ReleaseInfo:
    """Relevant information from a published GitHub release."""

    tag: str
    version: Version
    name: str
    url: str
    notes: str
    prerelease: bool


@dataclass(frozen=True, slots=True)
class UpdateCheckResult:
    """Result of comparing the installed and newest eligible releases."""

    current_version: Version
    latest_release: ReleaseInfo | None
    update_available: bool


class UpdateService:
    """Discover newer SephirothOS releases from GitHub."""

    def __init__(
        self,
        current_version: str = VERSION,
        release_channel: str = RELEASE_CHANNEL,
        *,
        fetch_releases: ReleaseFetcher | None = None,
        timeout: float = 5.0,
    ) -> None:
        try:
            self._current_version = Version(current_version)
        except InvalidVersion as error:
            raise ValueError(
                f"Invalid current application version: {current_version!r}."
            ) from error

        if release_channel not in {"alpha", "beta", "stable"}:
            raise ValueError(f"Unknown release channel: {release_channel!r}.")

        if timeout <= 0:
            raise ValueError("Update timeout must be greater than zero.")

        self._release_channel = release_channel
        self._timeout = timeout
        self._fetch_releases = fetch_releases or self._fetch_github_releases

    def check(self) -> UpdateCheckResult:
        """Return the newest release eligible for this installation."""

        try:
            payload = self._fetch_releases()
        except Exception as error:
            raise UpdateCheckError("Could not retrieve SephirothOS release information.") from error

        if not isinstance(payload, list):
            raise UpdateCheckError("GitHub returned an invalid releases response.")

        releases = tuple(
            release for item in payload if (release := self._parse_release(item)) is not None
        )

        eligible_releases = tuple(release for release in releases if self._is_eligible(release))

        latest_release = max(
            eligible_releases,
            key=lambda release: release.version,
            default=None,
        )

        return UpdateCheckResult(
            current_version=self._current_version,
            latest_release=latest_release,
            update_available=(
                latest_release is not None and latest_release.version > self._current_version
            ),
        )

    def _is_eligible(self, release: ReleaseInfo) -> bool:
        if self._release_channel == "stable":
            return not release.prerelease and not release.version.is_prerelease

        if self._release_channel == "beta":
            if not release.version.is_prerelease:
                return True

            prerelease = release.version.pre
            return prerelease is not None and prerelease[0] in {
                "b",
                "rc",
            }

        return True

    @staticmethod
    def _parse_release(payload: object) -> ReleaseInfo | None:
        if not isinstance(payload, dict):
            return None

        if payload.get("draft") is True:
            return None

        tag = payload.get("tag_name")

        if not isinstance(tag, str) or not tag.strip():
            return None

        try:
            version = Version(tag.removeprefix("v"))
        except InvalidVersion:
            return None

        raw_name = payload.get("name")
        raw_url = payload.get("html_url")
        raw_notes = payload.get("body")

        name = raw_name if isinstance(raw_name, str) and raw_name.strip() else tag
        url = raw_url if isinstance(raw_url, str) and raw_url.strip() else RELEASES_URL
        notes = raw_notes if isinstance(raw_notes, str) else ""

        return ReleaseInfo(
            tag=tag,
            version=version,
            name=name,
            url=url,
            notes=notes,
            prerelease=payload.get("prerelease") is True,
        )

    def _fetch_github_releases(self) -> object:
        request = Request(
            RELEASES_API_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": f"SephirothOS/{self._current_version}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

        with urlopen(
            request,
            timeout=self._timeout,
        ) as response:
            return json.load(response)
