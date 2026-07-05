# --- imports
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl

import assets.resource_rc as resources_rc

class BGMPlayer:
    def __init__(self):
        self.audio = QAudioOutput()
        self.player = QMediaPlayer()

        self.player.setAudioOutput(self.audio)
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio.setVolume(0.3)

        self.player.setSource(QUrl("qrc:///DefaultSoundtrack.mp3"))

    def start_music(self):
        print("[bgmp]: starting background music")
        self.player.play()
        print("[bgmp]: music started")