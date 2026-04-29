# Ahaa! Sesli Tepki Botu

Bazen kodun içinden çıkamazsınız, bazen de bir şeyi bir anda kavrarsınız ya... İşte o "aydınlanma" anını (Ahaa!) daha dramatik ve eğlenceli hale getirmek için bu botu yazdım. Kısacası, siz bir şeyi fark ettiğinizde bilgisayarınız da sizinle beraber şaşırıyor.

## 🎤 Olay Nedir?
Bu küçük Python scripti, arka planda pusuda bekler ve mikrofondan "Ahaa" dediğinizi duyduğu anda o meşhur sesi patlatır. Kendi başınıza bir şeyler çözerken gelen o sessiz gururu, sesli bir kutlamaya dönüştürür.

### Ses Kaynağı ve İlham
Projenin ruhunu anlamak ve sesin nereden geldiğini görmek için şu videoya bir göz atabilirsiniz:

[![Ahaa Video](https://img.youtube.com/vi/nG92hAZ5rrI/0.jpg)](https://www.youtube.com/watch?v=nG92hAZ5rrI)

## 📦 Kurulum ve Çalıştırma

İki farklı şekilde kullanabilirsiniz:

### 1. EXE Olarak (Hızlı Başlangıç)
Python kurmakla uğraşmak istemiyorsanız, `dist/AhaaBot.exe` dosyasını çalıştırabilirsiniz. Özel ikonu ve ses dosyası (mp3) içerisine gömülüdür, her yerde tek başına çalışabilir.

### 2. Python ile Çalıştırma
Geliştirme yapmak veya script olarak çalıştırmak isterseniz:

1. **Bağımlılıkları Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```
   *Not: Windows üzerinde PyAudio kurarken hata alırsanız `pip install pipwin` ve ardından `pipwin install pyaudio` komutlarını deneyebilirsiniz.*

2. **Çalıştırın:**
   ```bash
   python main.py
   ```

## 🛠 Teknik Detaylar
- **Kullanım:** Program başladığında ortam gürültüsünü analiz eder ve "Sistem hazır" mesajını verir. Sonrasında tek yapmanız gereken doğru anı yakalayıp "Ahaa" demek.
- **İnternet Bağlantısı:** Ses tanıma için Google API'sini kullanıyor, bu yüzden internet bağlantısı gereklidir.
- **Hassasiyet:** Kod içindeki `energy_threshold` değeriyle oynayarak botun ne kadar hassas olacağını ayarlayabilirsiniz.

---
Bir pazar günü can sıkıntısından doğan, hayat kalitenizi artırmasa da yüzünüzü güldüren küçük bir proje. Keyifli kullanımlar.
