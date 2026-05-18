import argparse
import logging
import os
import sys

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

from ahaa.app_config import BotConfig
from ahaa.app_factory import AhaaBotFactory


def configure_console_encoding():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


configure_console_encoding()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def parse_args():
    parser = argparse.ArgumentParser(description="Ahaa sesli tepki botu")
    parser.add_argument(
        "--list-audio",
        "--list-mics",
        action="store_true",
        help="Ses çıkış durumunu ve kayıt yapabilen mikrofonları listele",
    )
    parser.add_argument("--mic-index", type=int, help="Kullanılacak mikrofon index'i")
    parser.add_argument("--music", default="assets/ahaa.mp3", help="Çalınacak ses dosyası")
    parser.add_argument("--trigger", default="aha", help="Tetikleyici kelime")
    return parser.parse_args()


def log_audio_report(factory, preferred_index=None):
    devices, route_status, selected_microphone = factory.describe_audio(preferred_index)

    logging.info("Ses çıkış durumu: %s. %s", route_status.route.value, route_status.reason)
    if route_status.matched_device:
        logging.info(
            "Algılanan çıkış [%s]: %s",
            route_status.matched_device.index,
            route_status.matched_device.name,
        )

    logging.info("Kayıt yapabilen mikrofonlar:")
    for device in devices:
        if not device.can_record:
            continue

        selected_marker = " <- otomatik seçim" if device.index == selected_microphone.index else ""
        logging.info(
            "  [%s] %s | kanal=%s | rate=%s%s",
            device.index,
            device.name,
            device.input_channels,
            device.sample_rate,
            selected_marker,
        )


def main():
    args = parse_args()
    config = BotConfig(
        music_file=args.music,
        trigger_word=args.trigger,
        microphone_index=args.mic_index,
    )
    factory = AhaaBotFactory()

    if args.list_audio:
        log_audio_report(factory, args.mic_index)
        return 0

    bot = factory.create(config)
    bot.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
