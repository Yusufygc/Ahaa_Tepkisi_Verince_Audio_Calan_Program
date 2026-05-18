from ahaa.audio_devices import AudioDeviceRepository, HeadphoneDetector, MicrophoneSelector
from ahaa.bot import AhaaBot
from ahaa.music_player import MusicPlayer
from ahaa.speech_listener import SpeechListener


class AhaaBotFactory:
    def __init__(self, repository=None, detector=None, selector=None):
        self.repository = repository or AudioDeviceRepository()
        self.detector = detector or HeadphoneDetector()
        self.selector = selector or MicrophoneSelector()

    def create(self, config):
        devices = self.repository.list_devices()
        route_status = self.detector.detect(devices)
        input_devices = [device for device in devices if device.can_record]
        selected_microphone = self.selector.select(
            input_devices=input_devices,
            route_status=route_status,
            preferred_index=config.microphone_index,
        )
        listener = SpeechListener(
            microphone_index=selected_microphone.index,
            language=config.language,
        )
        player = MusicPlayer(config.music_file)

        return AhaaBot(
            config=config,
            selected_microphone=selected_microphone,
            route_status=route_status,
            listener=listener,
            player=player,
        )

    def describe_audio(self, preferred_index=None):
        devices = self.repository.list_devices()
        route_status = self.detector.detect(devices)
        input_devices = [device for device in devices if device.can_record]
        selected_microphone = self.selector.select(
            input_devices=input_devices,
            route_status=route_status,
            preferred_index=preferred_index,
        )
        return devices, route_status, selected_microphone
