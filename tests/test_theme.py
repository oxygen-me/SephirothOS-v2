import pytest

from sephirothos.services.display_scale import DisplayScaleService
from sephirothos.services.theme import (
    THEME_DISPLAY_NAMES,
    ThemeId,
    ThemeService,
    UnavailableThemeError,
    UnknownThemeError,
)


class FakeThemeTarget:
    def __init__(self) -> None:
        self.stylesheets: list[str] = []

    def setStyleSheet(self, stylesheet: str) -> None:
        self.stylesheets.append(stylesheet)


def make_service() -> tuple[
    ThemeService,
    FakeThemeTarget,
    DisplayScaleService,
]:
    target = FakeThemeTarget()
    scale = DisplayScaleService()
    service = ThemeService(target, scale)

    return service, target, scale


def test_void_is_the_default_theme() -> None:
    service, _, _ = make_service()

    assert service.theme_id is ThemeId.VOID
    assert service.display_name == "Void"


def test_all_requested_theme_names_are_registered() -> None:
    assert THEME_DISPLAY_NAMES == {
        ThemeId.VOID: "Void",
        ThemeId.SATAN: "Satan",
        ThemeId.RGB: "RGB",
        ThemeId.PISS: "Piss",
        ThemeId.BISEXUAL: "Bisexual",
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
    assert "#17171B" in target.stylesheets[0]
    assert "#8F4FFF" in target.stylesheets[0]


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


def test_scale_change_rebuilds_stylesheet() -> None:
    service, target, scale = make_service()
    service.apply_current()

    original = target.stylesheets[-1]

    scale.set_factor(1.5)

    assert len(target.stylesheets) == 2
    assert target.stylesheets[-1] != original
    assert "font-size: 21px" in target.stylesheets[-1]
