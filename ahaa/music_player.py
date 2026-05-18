import logging

import pygame

from ahaa.resources import resource_path


class MusicPlayer:
    def __init__(self, music_path):
        self.music_path = resource_path(music_path)
        pygame.mixer.init()

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def play(self):
        try:
            if self.is_playing():
                logging.info("Ses zaten çalıyor, yeniden başlatılıyor...")
                pygame.mixer.music.stop()

            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play()
            logging.info("Oynatılıyor: %s", self.music_path)
        except Exception as exc:
            logging.error("Müzik çalma hatası: %s", exc)
