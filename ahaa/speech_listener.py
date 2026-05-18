import speech_recognition as sr


class SpeechListener:
    def __init__(self, microphone_index, language):
        self.microphone_index = microphone_index
        self.language = language
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=microphone_index)
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.7
        self.recognizer.phrase_threshold = 0.2

    def open_source(self):
        return self.microphone

    def calibrate(self, source, duration):
        self.recognizer.adjust_for_ambient_noise(source, duration=duration)
        return self.recognizer.energy_threshold

    def listen(self, source, timeout, phrase_time_limit):
        return self.recognizer.listen(
            source,
            timeout=timeout,
            phrase_time_limit=phrase_time_limit,
        )

    def recognize(self, audio):
        return self.recognizer.recognize_google(audio, language=self.language).lower()
