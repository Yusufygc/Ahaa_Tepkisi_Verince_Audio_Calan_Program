from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import unicodedata

import speech_recognition as sr


class AudioRoute(Enum):
    HEADPHONES = "headphones"
    SPEAKERS = "speakers"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class AudioDevice:
    index: int
    name: str
    input_channels: int
    output_channels: int
    sample_rate: int

    @property
    def can_record(self):
        return self.input_channels > 0

    @property
    def can_play(self):
        return self.output_channels > 0


@dataclass(frozen=True)
class AudioRouteStatus:
    route: AudioRoute
    reason: str
    matched_device: Optional[AudioDevice] = None


class AudioDeviceRepository:
    def list_devices(self):
        devices = []
        audio = sr.Microphone.get_pyaudio().PyAudio()

        try:
            names = sr.Microphone.list_microphone_names()
            for index, name in enumerate(names):
                try:
                    device_info = audio.get_device_info_by_index(index)
                except Exception:
                    continue

                devices.append(
                    AudioDevice(
                        index=index,
                        name=self._repair_device_name(name),
                        input_channels=int(device_info.get("maxInputChannels", 0)),
                        output_channels=int(device_info.get("maxOutputChannels", 0)),
                        sample_rate=int(device_info.get("defaultSampleRate", 0)),
                    )
                )
        finally:
            audio.terminate()

        return devices

    def _repair_device_name(self, name):
        if not any(marker in name for marker in ("Ã", "Ä", "Å")):
            return name

        for encoding in ("cp1252", "latin1"):
            try:
                return name.encode(encoding).decode("utf-8")
            except UnicodeError:
                continue

        return name

    def list_input_devices(self):
        return [device for device in self.list_devices() if device.can_record]

    def list_output_devices(self):
        return [device for device in self.list_devices() if device.can_play]


class HeadphoneDetector:
    HEADPHONE_WORDS = ("headphone", "headset", "earphone", "earbuds", "kulakl")
    SPEAKER_WORDS = ("speaker", "hoparl")

    def detect(self, devices: List[AudioDevice]):
        output_devices = [device for device in devices if device.can_play]
        headphone_match = self._find_name_match(output_devices, self.HEADPHONE_WORDS)
        if headphone_match:
            return AudioRouteStatus(
                route=AudioRoute.HEADPHONES,
                reason="Kulaklık/headset çıkış aygıtı algılandı.",
                matched_device=headphone_match,
            )

        speaker_match = self._find_name_match(output_devices, self.SPEAKER_WORDS)
        if speaker_match:
            return AudioRouteStatus(
                route=AudioRoute.SPEAKERS,
                reason=(
                    "Hoparlör çıkışı algılandı. Analog jaklı kulaklıklar Windows'ta "
                    "bazen hoparlör olarak görünebilir."
                ),
                matched_device=speaker_match,
            )

        return AudioRouteStatus(
            route=AudioRoute.UNKNOWN,
            reason="Aktif çıkış tipini cihaz adından anlayamadım.",
        )

    def _find_name_match(self, devices, words):
        for device in devices:
            normalized_name = self._normalize(device.name)
            if any(word in normalized_name for word in words):
                return device
        return None

    def _normalize(self, value):
        normalized = unicodedata.normalize("NFKD", value.casefold())
        return "".join(char for char in normalized if not unicodedata.combining(char))


class MicrophoneSelector:
    MICROPHONE_WORDS = ("microphone", "mikrofon", "mic")
    HEADSET_WORDS = HeadphoneDetector.HEADPHONE_WORDS
    SYSTEM_WORDS = ("microsoft ses", "sound mapper", "birincil ses")
    OUTPUT_WORDS = ("output", "speaker", "hoparl")

    def select(self, input_devices, route_status, preferred_index=None):
        if not input_devices:
            raise RuntimeError("Kayıt yapabilen mikrofon bulunamadı.")

        if preferred_index is not None:
            return self._select_preferred(input_devices, preferred_index)

        candidates = self._without_system_devices(input_devices) or input_devices

        if route_status.route == AudioRoute.HEADPHONES:
            selected = self._find_by_words(candidates, self.HEADSET_WORDS)
            if selected:
                return selected

        selected = self._find_by_words(candidates, self.MICROPHONE_WORDS)
        if selected:
            return selected

        return candidates[0]

    def _select_preferred(self, input_devices, preferred_index):
        for device in input_devices:
            if device.index == preferred_index:
                return device

        available = ", ".join(str(device.index) for device in input_devices)
        raise RuntimeError(
            f"Seçilen mikrofon kayıt yapamıyor: {preferred_index}. "
            f"Kullanılabilir indexler: {available}"
        )

    def _without_system_devices(self, devices):
        return [
            device
            for device in devices
            if not any(word in self._normalize(device.name) for word in self.SYSTEM_WORDS)
        ]

    def _find_by_words(self, devices, words):
        for device in devices:
            normalized_name = self._normalize(device.name)
            if any(word in normalized_name for word in words) and not any(
                word in normalized_name for word in self.OUTPUT_WORDS
            ):
                return device
        return None

    def _normalize(self, value):
        normalized = unicodedata.normalize("NFKD", value.casefold())
        return "".join(char for char in normalized if not unicodedata.combining(char))
