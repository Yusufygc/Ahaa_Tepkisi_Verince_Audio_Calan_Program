import unittest

from ahaa.audio_devices import (
    AudioDevice,
    AudioRoute,
    HeadphoneDetector,
    MicrophoneSelector,
)


class HeadphoneDetectorTests(unittest.TestCase):
    def test_detects_headset_output_by_name(self):
        devices = [
            AudioDevice(1, "USB Headset", 0, 2, 48000),
            AudioDevice(2, "Built-in Microphone", 2, 0, 48000),
        ]

        status = HeadphoneDetector().detect(devices)

        self.assertEqual(AudioRoute.HEADPHONES, status.route)
        self.assertEqual("USB Headset", status.matched_device.name)

    def test_detects_speaker_output_by_name(self):
        devices = [AudioDevice(1, "Hoparlör", 0, 2, 44100)]

        status = HeadphoneDetector().detect(devices)

        self.assertEqual(AudioRoute.SPEAKERS, status.route)


class MicrophoneSelectorTests(unittest.TestCase):
    def test_skips_windows_sound_mapper_when_real_microphone_exists(self):
        input_devices = [
            AudioDevice(0, "Microsoft Ses Eslestiricisi - Input", 2, 0, 44100),
            AudioDevice(1, "Mikrofon (C-Media Audio)", 2, 0, 44100),
        ]

        selected = MicrophoneSelector().select(
            input_devices,
            HeadphoneDetector().detect([]),
        )

        self.assertEqual(1, selected.index)

    def test_headphone_route_prefers_headset_microphone(self):
        input_devices = [
            AudioDevice(1, "Mikrofon (C-Media Audio)", 2, 0, 44100),
            AudioDevice(2, "USB Headset Microphone", 2, 0, 48000),
        ]
        route_status = HeadphoneDetector().detect(
            [AudioDevice(3, "USB Headset", 0, 2, 48000)]
        )

        selected = MicrophoneSelector().select(input_devices, route_status)

        self.assertEqual(2, selected.index)


if __name__ == "__main__":
    unittest.main()
