"""User-controlled SephirothOS display scaling."""

from __future__ import annotations

import math

from PySide6.QtCore import QObject, Signal

SUPPORTED_SCALE_FACTORS = (
    0.8,
    1.0,
    1.1,
    1.25,
    1.5,
    1.75,
    2.0,
)


class DisplayScaleError(ValueError):
    """Raised when an unsupported display scale is requested."""


class DisplayScaleService(QObject):
    """Own the user-selected SephirothOS interface scale."""

    scale_changed = Signal(float)

    def __init__(
        self,
        initial_factor: float = 1.0,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._factor = self._validated_factor(initial_factor)

    @property
    def factor(self) -> float:
        """Return the active scale factor."""

        return self._factor

    @property
    def percentage(self) -> int:
        """Return the active scale factor as a percentage."""

        return round(self._factor * 100)

    @property
    def supported_factors(self) -> tuple[float, ...]:
        """Return the supported user-selected scale factors."""

        return SUPPORTED_SCALE_FACTORS

    def set_factor(self, factor: float) -> bool:
        """
        Apply a supported scale factor.

        Returns True when the active factor changed and False when the
        requested factor was already active.
        """

        validated = self._validated_factor(factor)

        if math.isclose(validated, self._factor):
            return False

        self._factor = validated
        self.scale_changed.emit(self._factor)
        return True

    def scale_value(self, value: int | float) -> float:
        """Scale a numeric design value without rounding it."""

        self._validate_design_value(value)
        return float(value) * self._factor

    def scale_pixels(self, value: int | float) -> int:
        """Scale and round a non-negative pixel measurement."""

        scaled = self.scale_value(value)
        return int(scaled + 0.5)

    @staticmethod
    def _validate_design_value(value: int | float) -> None:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("The design value must be numeric.")

        if value < 0:
            raise ValueError("The design value must be non-negative.")

    @staticmethod
    def _validated_factor(factor: float) -> float:
        if isinstance(factor, bool) or not isinstance(factor, int | float):
            raise DisplayScaleError("Display scale must be numeric.")

        numeric_factor = float(factor)

        for supported_factor in SUPPORTED_SCALE_FACTORS:
            if math.isclose(numeric_factor, supported_factor):
                return supported_factor

        percentages = ", ".join(f"{round(item * 100)}%" for item in SUPPORTED_SCALE_FACTORS)

        raise DisplayScaleError(
            f"Unsupported scale factor {numeric_factor:g}. Supported scales: {percentages}."
        )
