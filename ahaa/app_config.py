from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BotConfig:
    music_file: str = "assets/ahaa.mp3"
    trigger_word: str = "aha"
    microphone_index: Optional[int] = None
    calibration_seconds: float = 1.0
    listen_timeout_seconds: float = 1.0
    phrase_time_limit_seconds: float = 3.0
    language: str = "tr-TR"
