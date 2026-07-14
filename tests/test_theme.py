import pytest

import sephirothos.services.theme as theme_module
from sephirothos.services.display_scale import DisplayScaleService
from sephirothos.services.theme import (
    ACCENT_DISPLAY_NAMES,
    THEME_DISPLAY_NAMES,
    AccentId,
    ThemeId,
    ThemeService,
    UnavailableAccentError,
    UnavailableThemeError,
    UnknownAccentError,
    UnknownThemeError,
)
from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.styles import (
    VOID_PALETTE,
    AccentPalette,
)


class FakeThemeTarget:
    def __init__(self) -> None:
        self.stylesheets: list[str] = []

    def setStyleSheet(self, stylesheet: str) -> None:
        self.stylesheets.append(stylesheet)


def make_service() -> tuple[
    ThemeService,
    FakeThemeTarget,
    UiMetrics,
]:
    target = FakeThemeTarget()
    scale = DisplayScaleService()
    metrics = UiMetrics.from_scale(scale)

    service = ThemeService(
        target=target,
        metrics=metrics,
    )

    return service, target, metrics


def test_void_and_purple_are_defaults() -> None:
    service, _, _ = make_service()

    assert service.theme_id is ThemeId.VOID
    assert service.accent_id is AccentId.PURPLE
    assert service.display_name == "Void"
    assert service.accent_display_name == "Purple"


def test_all_requested_theme_names_are_registered() -> None:
    assert THEME_DISPLAY_NAMES == {
        ThemeId.VOID: "Void",
        ThemeId.SATAN: "Satan",
        ThemeId.RGB: "RGB",
        ThemeId.PISS: "Piss",
        ThemeId.BISEXUAL: "Bisexual",
    }


def test_all_requested_accent_names_are_registered() -> None:
    assert ACCENT_DISPLAY_NAMES == {
        AccentId.PURPLE: "Purple",
        AccentId.BLUE: "Blue",
        AccentId.LIGHT_BLUE: "Light Blue",
        AccentId.TEAL: "Teal",
        AccentId.GREEN: "Green",
        AccentId.YELLOW: "Yellow",
        AccentId.ORANGE: "Orange",
        AccentId.RED: "Red",
    }


def test_only_void_is_available_initially() -> None:
    service, _, _ = make_service()

    assert service.available_themes == (ThemeId.VOID,)
    assert service.is_available(ThemeId.VOID) is True
    assert service.is_available(ThemeId.SATAN) is False


def test_apply_current_sets_stylesheet() -> None:
    service, target, _ = make_service()

    service.apply_current()

    assert len(target.stylesheets) == 1
    assert VOID_PALETTE.background in target.stylesheets[0]
    assert VOID_PALETTE.accent in target.stylesheets[0]


def test_setting_current_theme_does_not_reapply() -> None:
    service, target, _ = make_service()

    changed = service.set_theme(ThemeId.VOID)

    assert changed is False
    assert target.stylesheets == []


def test_unknown_theme_is_rejected() -> None:
    service, _, _ = make_service()

    with pytest.raises(UnknownThemeError):
        service.set_theme("something-else")


def test_known_but_unavailable_theme_is_rejected() -> None:
    service, _, _ = make_service()

    with pytest.raises(UnavailableThemeError):
        service.set_theme(ThemeId.BISEXUAL)


def test_stylesheet_uses_supplied_metrics() -> None:
    service, target, metrics = make_service()

    service.apply_current()

    stylesheet = target.stylesheets[-1]

    assert f"font-size: {metrics.font_small}px" in stylesheet
    assert f"border: {metrics.border_thin}px solid" in stylesheet


def test_only_purple_accent_is_available_initially() -> None:
    service, _, _ = make_service()

    assert service.available_accents == (AccentId.PURPLE,)
    assert service.is_accent_available(
        AccentId.PURPLE,
    )
    assert not service.is_accent_available(
        AccentId.BLUE,
    )


def test_unknown_accent_is_rejected() -> None:
    service, _, _ = make_service()

    with pytest.raises(UnknownAccentError):
        service.set_accent("radioactive-beige")


def test_known_but_unavailable_accent_is_rejected() -> None:
    service, _, _ = make_service()

    with pytest.raises(UnavailableAccentError):
        service.set_accent(AccentId.BLUE)


def test_available_accent_is_applied(
    monkeypatch,
) -> None:
    test_accent = AccentPalette(
        base="#123456",
        hover="#234567",
        pressed="#012345",
        focus="#345678",
        glow="rgba(18, 52, 86, 0.20)",
    )

    monkeypatch.setitem(
        theme_module.AVAILABLE_ACCENTS,
        AccentId.BLUE,
        test_accent,
    )

    target = FakeThemeTarget()
    metrics = UiMetrics.from_scale(
        DisplayScaleService(),
    )
    service = ThemeService(
        target=target,
        metrics=metrics,
        initial_accent=AccentId.BLUE,
    )

    service.apply_current()

    stylesheet = target.stylesheets[-1]

    assert test_accent.base in stylesheet
    assert test_accent.hover in stylesheet
    assert test_accent.pressed in stylesheet


def test_setting_current_accent_does_not_reapply() -> None:
    service, target, _ = make_service()

    changed = service.set_accent(
        AccentId.PURPLE,
    )

    assert changed is False
    assert target.stylesheets == []
