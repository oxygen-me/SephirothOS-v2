"""SephirothOS background music playback."""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, QUrl
from PySide6.QtMultimedia import (
    QAudioOutput,
    QMediaPlayer,
)

logger = logging.getLogger(__name__)


class BackgroundMusicPlayer(QObject):
    """Own looping application background-music playback."""

    def __init__(
        self,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self.audio_output = QAudioOutput(self)
        self.media_player = QMediaPlayer(self)

        self.audio_output.setVolume(0.3)

        self.media_player.setAudioOutput(
            self.audio_output,
        )
        self.media_player.setLoops(
            QMediaPlayer.Loops.Infinite,
        )
        self.media_player.setSource(
            QUrl(
                "qrc:/bgm/BundledSoundtrack2.mp3",
            )
        )
        self.media_player.errorOccurred.connect(
            self._handle_error,
        )

    def play(self) -> None:
        """Begin or resume background-music playback."""

        self.media_player.play()
        logger.info("Background music playback requested")

    def stop(self) -> None:
        """Stop background-music playback."""

        self.media_player.stop()

    def set_volume(
        self,
        volume: float,
    ) -> None:
        """Set normalized playback volume."""

        if not 0.0 <= volume <= 1.0:
            raise ValueError("Background-music volume must be between 0.0 and 1.0.")

        self.audio_output.setVolume(volume)

    def _handle_error(
        self,
        error: QMediaPlayer.Error,
        message: str,
    ) -> None:
        logger.error(
            "Background music failed: %s (%s)",
            message,
            error.name,
        )
