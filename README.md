# Ahaa! Sesli Tepki Botu

Bazen kodun içinden çıkamazsınız, bazen de bir şeyi bir anda kavrarsınız ya... İşte o "aydınlanma" anını (Ahaa!) daha dramatik ve eğlenceli hale getirmek için bu botu yazdım. Kısacası, siz bir şeyi fark ettiğinizde bilgisayarınız da sizinle beraber şaşırıyor.

## Olay Nedir?
Bu küçük Python scripti, arka planda bekler ve mikrofondan "Ahaa" dediğinizi duyduğu anda o meşhur sesi çalar.

### Ses Kaynağı ve İlham
Projenin ruhunu anlamak ve sesin nereden geldiğini görmek için şu videoya bakabilirsiniz:

[![Ahaa Video](https://img.youtube.com/vi/nG92hAZ5rrI/0.jpg)](https://www.youtube.com/watch?v=nG92hAZ5rrI)

## Kurulum ve Çalıştırma

### 1. EXE Olarak
Python kurmakla uğraşmak istemiyorsanız `dist/AhaaBot.exe` dosyasını çalıştırabilirsiniz.

### 2. Python ile
Bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

Windows üzerinde PyAudio kurarken hata alırsanız `pip install pipwin` ve ardından `pipwin install pyaudio` komutlarını deneyebilirsiniz.

Çalıştırın:

```bash
python main.py
```

### Kulaklık Algılama
Program kulaklık/headset çıkışını cihaz adından otomatik algılar. Kulaklık algılanırsa headset mikrofonunu önceliklendirir; algılanmazsa Windows'un genel ses eşleştiricisi yerine gerçek mikrofon girişini seçmeye çalışır.

Ses durumunu ve seçilecek mikrofonu görmek için:

```bash
python main.py --list-audio
```

Gerekirse belirli bir mikrofon index'i verin:

```bash
python main.py --mic-index 1
```

Not: Analog jaklı kulaklıklar bazı Windows sistemlerinde hâlâ "Hoparlör" olarak görünebilir. Bu durumda program durumu raporlar ve gerçek mikrofon girişini seçmeye devam eder.

## Teknik Detaylar
- Uygulama kodu `ahaa/`, medya dosyaları `assets/`, testler `tests/` altında tutulur.
- Ses tanıma için Google API kullanılır, internet bağlantısı gerekir.
- `--list-mics` eski kullanım için `--list-audio` ile aynı işi yapmaya devam eder.
- Dinleme döngüsünde timeout vardır; yanlış cihaz seçilirse uygulama sessizce kilitlenmez.
