"""Remote announcement retrieval, validation, and caching."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from packaging.version import InvalidVersion, Version

from sephirothos.metadata import VERSION
from sephirothos.paths import cache_directory

ANNOUNCEMENT_SCHEMA_VERSION = 1
ANNOUNCEMENT_CACHE_FILENAME = "announcements.json"

# Change rewrite/alpha-1 to master when the rewrite replaces master.
ANNOUNCEMENTS_URL = (
    "https://raw.githubusercontent.com/"
    "oxygen-me/SephirothOS-v2/"
    "refs/heads/rewrite/alpha-1/"
    "remote/announcements.json"
)

AnnouncementFetcher = Callable[[], object]

logger = logging.getLogger(__name__)


class AnnouncementError(RuntimeError):
    """Base exception for announcement failures."""


class AnnouncementValidationError(AnnouncementError):
    """Raised when an announcement feed is invalid."""


class AnnouncementLoadError(AnnouncementError):
    """Raised when neither remote nor cached announcements can be loaded."""


class AnnouncementSource(StrEnum):
    """Origin of a successfully loaded announcement feed."""

    REMOTE = "remote"
    CACHE = "cache"


@dataclass(frozen=True, slots=True)
class Announcement:
    """Validated announcement displayed by SephirothOS."""

    identifier: str
    title: str
    body: str
    published_at: datetime
    minimum_version: Version | None
    maximum_version: Version | None
    action_url: str | None


@dataclass(frozen=True, slots=True)
class AnnouncementFeed:
    """Collection of announcements and its source."""

    announcements: tuple[Announcement, ...]
    source: AnnouncementSource


class AnnouncementService:
    """Load applicable announcements from GitHub or a local cache."""

    def __init__(
        self,
        current_version: str = VERSION,
        cache_path: Path | None = None,
        *,
        fetch_announcements: AnnouncementFetcher | None = None,
        timeout: float = 5.0,
    ) -> None:
        try:
            self._current_version = Version(current_version)
        except InvalidVersion as error:
            raise ValueError(
                f"Invalid current application version: {current_version!r}."
            ) from error

        if timeout <= 0:
            raise ValueError("Announcement timeout must be greater than zero.")

        self._cache_path = (
            cache_directory() / ANNOUNCEMENT_CACHE_FILENAME if cache_path is None else cache_path
        )
        self._timeout = timeout
        self._fetch_announcements = fetch_announcements or self._fetch_remote

    def load(self) -> AnnouncementFeed:
        """Load announcements, falling back to the last valid cache."""

        try:
            payload = self._fetch_announcements()
            announcements = self._parse_feed(payload)
        except Exception as remote_error:
            logger.warning(
                "Could not load remote announcements; trying cache.",
                exc_info=True,
            )

            try:
                cached_payload = self._read_cache()
                cached_announcements = self._parse_feed(
                    cached_payload,
                )
            except Exception:
                logger.warning(
                    "Could not load cached announcements.",
                    exc_info=True,
                )
                raise AnnouncementLoadError(
                    "No valid announcement feed is available."
                ) from remote_error

            return AnnouncementFeed(
                announcements=cached_announcements,
                source=AnnouncementSource.CACHE,
            )

        try:
            self._write_cache(payload)
        except OSError:
            # A cache failure should not discard valid remote content.
            logger.warning(
                "Could not cache the announcement feed.",
                exc_info=True,
            )

        return AnnouncementFeed(
            announcements=announcements,
            source=AnnouncementSource.REMOTE,
        )

    def _parse_feed(
        self,
        payload: object,
    ) -> tuple[Announcement, ...]:
        if not isinstance(payload, dict):
            raise AnnouncementValidationError("Announcement feed must be a JSON object.")

        schema_version = payload.get("schema_version")

        if not isinstance(schema_version, int) or isinstance(schema_version, bool):
            raise AnnouncementValidationError("Announcement schema_version must be an integer.")

        if schema_version != ANNOUNCEMENT_SCHEMA_VERSION:
            raise AnnouncementValidationError(f"Unsupported announcement schema: {schema_version}.")

        raw_announcements = payload.get("announcements")

        if not isinstance(raw_announcements, list):
            raise AnnouncementValidationError(
                "Announcement feed must contain an announcements list."
            )

        announcements: list[_ParsedAnnouncement] = []
        identifiers: set[str] = set()

        for index, raw_announcement in enumerate(raw_announcements):
            announcement = self._parse_announcement(
                raw_announcement,
                index,
            )

            if announcement.identifier in identifiers:
                raise AnnouncementValidationError(
                    f"Announcement identifiers must be unique: {announcement.identifier!r}."
                )

            identifiers.add(announcement.identifier)

            if announcement.enabled:
                announcements.append(announcement)

        applicable = tuple(
            announcement for announcement in announcements if self._is_applicable(announcement)
        )

        return tuple(
            sorted(
                applicable,
                key=lambda announcement: announcement.published_at,
                reverse=True,
            )
        )

    def _parse_announcement(
        self,
        payload: object,
        index: int,
    ) -> _ParsedAnnouncement:
        if not isinstance(payload, dict):
            raise AnnouncementValidationError(f"Announcement at index {index} must be an object.")

        identifier = self._required_text(
            payload,
            "id",
            index,
        )
        title = self._required_text(
            payload,
            "title",
            index,
        )
        body = self._required_text(
            payload,
            "body",
            index,
        )

        enabled = payload.get("enabled")

        if not isinstance(enabled, bool):
            raise AnnouncementValidationError(
                f"Announcement {identifier!r} must have a boolean enabled value."
            )

        published_at = self._parse_datetime(
            payload.get("published_at"),
            identifier,
        )
        minimum_version = self._parse_optional_version(
            payload.get("minimum_version"),
            "minimum_version",
            identifier,
        )
        maximum_version = self._parse_optional_version(
            payload.get("maximum_version"),
            "maximum_version",
            identifier,
        )
        action_url = self._parse_action_url(
            payload.get("action_url"),
            identifier,
        )

        if (
            minimum_version is not None
            and maximum_version is not None
            and minimum_version > maximum_version
        ):
            raise AnnouncementValidationError(
                f"Announcement {identifier!r} has an invalid version range."
            )

        return _ParsedAnnouncement(
            identifier=identifier,
            title=title,
            body=body,
            published_at=published_at,
            enabled=enabled,
            minimum_version=minimum_version,
            maximum_version=maximum_version,
            action_url=action_url,
        )

    def _is_applicable(
        self,
        announcement: Announcement,
    ) -> bool:
        if (
            announcement.minimum_version is not None
            and self._current_version < announcement.minimum_version
        ):
            return False

        return not (
            announcement.maximum_version is not None
            and self._current_version > announcement.maximum_version
        )

    @staticmethod
    def _required_text(
        payload: dict,
        key: str,
        index: int,
    ) -> str:
        value = payload.get(key)

        if not isinstance(value, str) or not value.strip():
            raise AnnouncementValidationError(
                f"Announcement at index {index} requires non-empty {key!r}."
            )

        return value.strip()

    @staticmethod
    def _parse_datetime(
        value: object,
        identifier: str,
    ) -> datetime:
        if not isinstance(value, str):
            raise AnnouncementValidationError(f"Announcement {identifier!r} requires published_at.")

        try:
            parsed = datetime.fromisoformat(value)
        except ValueError as error:
            raise AnnouncementValidationError(
                f"Announcement {identifier!r} has an invalid published_at value."
            ) from error

        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise AnnouncementValidationError(
                f"Announcement {identifier!r} published_at must include a timezone."
            )

        return parsed.astimezone(UTC)

    @staticmethod
    def _parse_optional_version(
        value: object,
        field_name: str,
        identifier: str,
    ) -> Version | None:
        if value is None:
            return None

        if not isinstance(value, str):
            raise AnnouncementValidationError(
                f"Announcement {identifier!r} {field_name} must be a string or null."
            )

        try:
            return Version(value)
        except InvalidVersion as error:
            raise AnnouncementValidationError(
                f"Announcement {identifier!r} has invalid {field_name}."
            ) from error

    @staticmethod
    def _parse_action_url(
        value: object,
        identifier: str,
    ) -> str | None:
        if value is None:
            return None

        if not isinstance(value, str):
            raise AnnouncementValidationError(
                f"Announcement {identifier!r} action_url must be a string or null."
            )

        parsed = urlparse(value)

        if parsed.scheme != "https" or not parsed.netloc:
            raise AnnouncementValidationError(
                f"Announcement {identifier!r} action_url must use HTTPS."
            )

        return value

    def _fetch_remote(self) -> object:
        request = Request(
            ANNOUNCEMENTS_URL,
            headers={
                "Accept": "application/json",
                "User-Agent": f"SephirothOS/{self._current_version}",
            },
        )

        with urlopen(
            request,
            timeout=self._timeout,
        ) as response:
            return json.load(response)

    def _read_cache(self) -> object:
        with self._cache_path.open(
            "r",
            encoding="utf-8",
        ) as cache_file:
            return json.load(cache_file)

    def _write_cache(self, payload: object) -> None:
        self._cache_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_path: Path | None = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self._cache_path.parent,
                prefix="announcements-",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                json.dump(
                    payload,
                    temporary_file,
                    indent=4,
                    ensure_ascii=False,
                )
                temporary_file.write("\n")
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
                temporary_path = Path(temporary_file.name)

            os.replace(
                temporary_path,
                self._cache_path,
            )
        except OSError:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

            raise


@dataclass(frozen=True, slots=True)
class _ParsedAnnouncement(Announcement):
    """Internal announcement representation retaining enabled state."""

    enabled: bool
