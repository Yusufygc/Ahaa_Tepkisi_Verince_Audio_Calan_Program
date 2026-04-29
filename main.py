import speech_recognition as sr
import pygame
import logging
import time
import sys

# 1. LOGLAMA YAPILANDIRMASI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class AhaaBot:
    def __init__(self, music_path, trigger_word="aha"):
        self.music_path = resource_path(music_path)
        self.trigger_word = trigger_word
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Pygame başlatma
        pygame.mixer.init()
        
        # Hassasiyet ayarları
        self.recognizer.energy_threshold = 300  # Ortam sesine göre otomatik ayarlanacak
        self.recognizer.dynamic_energy_threshold = True

    def is_playing(self):
        """Müziğin şu an çalıp çalmadığını kontrol eder."""
        return pygame.mixer.music.get_busy()

    def play_music(self):
        """Müziği başlatır veya zaten çalıyorsa yeniden başlatır."""
        try:
            if self.is_playing():
                logging.info("Şarkı zaten çalıyor, yeniden başlatılıyor...")
                pygame.mixer.music.stop()
            
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play()
            logging.info(f"Oynatılıyor: {self.music_path}")
        except Exception as e:
            logging.error(f"Müzik çalma hatası: {e}")

    def listen_and_process(self):
        """Sürekli dinleme döngüsü."""
        with self.microphone as source:
            logging.info("Ortam sesi analiz ediliyor... Lütfen kısa bir süre sessiz kalın.")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            logging.info("Sistem hazır! 'Ahaa' demenizi bekliyorum (Çıkmak için Ctrl+C).")

            while True:
                try:
                    # phrase_time_limit: Kısa kelimeler için dinleme süresini kısıtlar
                    audio = self.recognizer.listen(source, phrase_time_limit=3)
                    
                    # Google Ses Tanıma (Alternatif olarak çevrimdışı Vosk kullanılabilir)
                    text = self.recognizer.recognize_google(audio, language="tr-TR").lower()
                    logging.info(f"Duyulan: '{text}'")

                    if self.trigger_word in text:
                        logging.info(">>> Tetikleyici yakalandı!")
                        self.play_music()

                except sr.UnknownValueError:
                    # Ses anlaşılamadığında veya sessizlikte hiçbir şey yapma
                    pass
                except sr.RequestError as e:
                    logging.error(f"Servis hatası (İnternet bağlantısını kontrol edin): {e}")
                    time.sleep(5) # Hata durumunda sistemi yormamak için bekle
                except KeyboardInterrupt:
                    logging.info("Program kullanıcı tarafından kapatılıyor...")
                    break
                except Exception as e:
                    logging.error(f"Beklenmedik hata: {e}")

# 2. ÇALIŞTIRMA BÖLÜMÜ
if __name__ == "__main__":
    # AYARLAR
    MUSIC_FILE = "ahaa.mp3"  # Müziğinin dosya adını buraya yaz
    TRIGGER = "aha"             # Tetikleyici kelime
    
    bot = AhaaBot(music_path=MUSIC_FILE, trigger_word=TRIGGER)
    bot.listen_and_process()