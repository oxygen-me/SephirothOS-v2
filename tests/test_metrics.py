from dataclasses import fields

import pytest

from sephirothos.services.display_scale import DisplayScaleService
from sephirothos.ui.metrics import UiMetrics

BASE_SPACING = {
    "space_5": 5,
    "space_10": 10,
    "space_15": 15,
    "space_20": 20,
    "space_25": 25,
    "space_30": 30,
    "space_40": 40,
    "space_50": 50,
    "space_60": 60,
}

BASE_TYPOGRAPHY = {
    "font_caption": 12,
    "font_small": 14,
    "font_body": 16,
    "font_subtitle": 18,
    "font_emphasis": 24,
    "font_hero_subtitle": 32,
    "font_page_title": 36,
    "font_hero_title": 60,
}


def test_default_metrics_preserve_base_five_spacing() -> None:
    metrics = UiMetrics.from_scale(DisplayScaleService(1.0))

    for name, expected in BASE_SPACING.items():
        assert getattr(metrics, name) == expected


def test_default_metrics_preserve_typography_scale() -> None:
    metrics = UiMetrics.from_scale(DisplayScaleService(1.0))

    for name, expected in BASE_TYPOGRAPHY.items():
        assert getattr(metrics, name) == expected


@pytest.mark.parametrize("factor", [1.1, 1.25, 1.5, 1.75, 2.0])
def test_spacing_uses_display_scale(factor: float) -> None:
    scale = DisplayScaleService(factor)
    metrics = UiMetrics.from_scale(scale)

    for name, base_value in BASE_SPACING.items():
        assert getattr(metrics, name) == scale.scale_pixels(base_value)


@pytest.mark.parametrize("factor", [1.1, 1.25, 1.5, 1.75, 2.0])
def test_typography_uses_display_scale(factor: float) -> None:
    scale = DisplayScaleService(factor)
    metrics = UiMetrics.from_scale(scale)

    for name, base_value in BASE_TYPOGRAPHY.items():
        assert getattr(metrics, name) == scale.scale_pixels(base_value)


def test_all_resolved_metrics_are_integers() -> None:
    metrics = UiMetrics.from_scale(DisplayScaleService(1.25))

    for field in fields(metrics):
        value = getattr(metrics, field.name)

        assert isinstance(value, int), field.name


def test_borders_remain_visible() -> None:
    metrics = UiMetrics.from_scale(DisplayScaleService(1.0))

    assert metrics.border_thin >= 1
    assert metrics.border_strong >= 2


def test_shell_geometry_is_scaled() -> None:
    default = UiMetrics.from_scale(DisplayScaleService(1.0))
    enlarged = UiMetrics.from_scale(DisplayScaleService(1.5))

    assert enlarged.top_bar_height > default.top_bar_height
    assert enlarged.sidebar_width > default.sidebar_width


def test_component_geometry_is_scaled() -> None:
    default = UiMetrics.from_scale(DisplayScaleService(1.0))
    enlarged = UiMetrics.from_scale(DisplayScaleService(2.0))

    assert enlarged.scrollbar_extent > default.scrollbar_extent
    assert enlarged.checkbox_extent > default.checkbox_extent
    assert enlarged.progress_height > default.progress_height
