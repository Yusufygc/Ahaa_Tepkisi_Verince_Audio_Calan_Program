import logging
import time

import speech_recognition as sr


class AhaaBot:
    def __init__(self, config, selected_microphone, route_status, listener, player):
        self.config = config
        self.selected_microphone = selected_microphone
        self.route_status = route_status
        self.listener = listener
        self.player = player
        self.empty_listen_count = 0

    def run(self):
        self._log_audio_status()

        with self.listener.open_source() as source:
            logging.info("Ortam sesi analiz ediliyor. Lütfen kısa bir süre sessiz kalın.")
            threshold = self.listener.calibrate(source, self.config.calibration_seconds)
            logging.info(
                "Sistem hazır. Eşik: %.0f. '%s' bekleniyor. Çıkmak için Ctrl+C.",
                threshold,
                self.config.trigger_word,
            )

            while True:
                try:
                    audio = self.listener.listen(
                        source,
                        timeout=self.config.listen_timeout_seconds,
                        phrase_time_limit=self.config.phrase_time_limit_seconds,
                    )
                    self.empty_listen_count = 0
                    text = self.listener.recognize(audio)
                    logging.info("Duyulan: '%s'", text)

                    if self.config.trigger_word.lower() in text:
                        logging.info(">>> Tetikleyici yakalandı.")
                        self.player.play()

                except sr.WaitTimeoutError:
                    self._handle_empty_listen()
                except sr.UnknownValueError:
                    logging.info("Ses alındı ama anlaşılamadı.")
                except sr.RequestError as exc:
                    logging.error(
                        "Servis hatası. İnternet bağlantısını kontrol edin: %s",
                        exc,
                    )
                    time.sleep(5)
                except KeyboardInterrupt:
                    logging.info("Program kullanıcı tarafından kapatılıyor...")
                    break
                except Exception as exc:
                    logging.exception("Beklenmedik hata: %s", exc)

    def _log_audio_status(self):
        logging.info(
            "Ses çıkış durumu: %s. %s",
            self.route_status.route.value,
            self.route_status.reason,
        )
        if self.route_status.matched_device:
            logging.info(
                "Algılanan çıkış [%s]: %s",
                self.route_status.matched_device.index,
                self.route_status.matched_device.name,
            )

        logging.info(
            "Kullanılan mikrofon [%s]: %s",
            self.selected_microphone.index,
            self.selected_microphone.name,
        )

    def _handle_empty_listen(self):
        self.empty_listen_count += 1
        if self.empty_listen_count == 5:
            logging.info(
                "Henüz ses algılanmadı. Kulaklık takılıysa mikrofon kaynağı "
                "değişmiş olabilir; 'python main.py --list-audio' ile kontrol edin."
            )
        elif self.empty_listen_count % 30 == 0:
            logging.info("Dinleme devam ediyor, ses bekleniyor...")
