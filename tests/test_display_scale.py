import pytest

from sephirothos.services.display_scale import (
    SUPPORTED_SCALE_FACTORS,
    DisplayScaleError,
    DisplayScaleService,
)


def test_default_scale_is_one_hundred_percent() -> None:
    service = DisplayScaleService()

    assert service.factor == 1.0
    assert service.percentage == 100


def test_supported_scale_can_be_selected() -> None:
    service = DisplayScaleService()

    changed = service.set_factor(1.25)

    assert changed is True
    assert service.factor == 1.25
    assert service.percentage == 125


def test_setting_current_scale_does_not_emit_change() -> None:
    service = DisplayScaleService(1.25)
    emitted: list[float] = []

    service.scale_changed.connect(emitted.append)

    changed = service.set_factor(1.25)

    assert changed is False
    assert emitted == []


def test_scale_change_emits_new_factor() -> None:
    service = DisplayScaleService()
    emitted: list[float] = []

    service.scale_changed.connect(emitted.append)

    service.set_factor(1.5)

    assert emitted == [1.5]


@pytest.mark.parametrize("factor", SUPPORTED_SCALE_FACTORS)
def test_all_declared_scale_factor_are_accepted(factor: float) -> None:
    service = DisplayScaleService(factor)

    assert service.factor == factor


@pytest.mark.parametrize(
    "factor",
    [
        0,
        0.5,
        1.2,
        2.5,
        -1,
        True,
        "1.25",
    ],
)
def test_unsupported_scale_is_rejected(factor) -> None:
    with pytest.raises(DisplayScaleError):
        DisplayScaleService(factor)


def test_pixel_measurement_is_scaled_and_rounded() -> None:
    service = DisplayScaleService(1.25)

    assert service.scale_pixels(20) == 25
    assert service.scale_pixels(5) == 6


def test_unrounded_measurement_is_available() -> None:
    service = DisplayScaleService(1.1)

    assert service.scale_value(15) == pytest.approx(16.5)


def test_negative_design_value_is_rejected() -> None:
    service = DisplayScaleService()

    with pytest.raises(ValueError):
        service.scale_pixels(-10)


def test_boolean_design_value_is_rejected() -> None:
    service = DisplayScaleService()

    with pytest.raises(TypeError):
        service.scale_pixels(True)
