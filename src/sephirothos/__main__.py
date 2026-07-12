"""Executable entry point for SephirothOS."""

from __future__ import annotations

import sys

from sephirothos.application import SephirothApplication
from sephirothos.config import ConfigurationError
from sephirothos.paths import PathConfigurationError
from sephirothos.services.display_scale import DisplayScaleError
from sephirothos.services.theme import ThemeError


def main() -> int:
    try:
        application = SephirothApplication(sys.argv)
    except (
        ConfigurationError,
        DisplayScaleError,
        PathConfigurationError,
        ThemeError,
    ) as error:
        print(f"SephirothOS could not start {error}", file=sys.stderr)
        return 1

    return application.run()


if __name__ == "__main__":
    raise SystemExit(main())
