"""Reusable card containers."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

from sephirothos.ui.metrics import UiMetrics
from sephirothos.ui.roles import SurfaceRole


class Card(QWidget):
    """Base container providing standardized card presentation."""

    def __init__(
        self,
        metrics: UiMetrics,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )
        self.setProperty("surfaceRole", SurfaceRole.CARD.value)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            metrics.space_20,
            metrics.space_20,
            metrics.space_20,
            metrics.space_20,
        )
        self.main_layout.setSpacing(metrics.space_20)
