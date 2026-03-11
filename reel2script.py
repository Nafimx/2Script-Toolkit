#!/usr/bin/env python3
"""
reel2script.py — part of the 2script-toolkit
─────────────────────────────────────────────
Paste an Instagram reel URL → get a clean, editable transcript in ~30 seconds.
100% free. Runs locally. No API keys. No subscriptions.

REQUIRES: instagram_cookies.txt in the same folder as this script.
HOW TO GET IT:
  1. Install "Get cookies.txt LOCALLY" extension in Chrome
  2. Go to instagram.com (logged in)
  3. Click extension → select instagram.com → Export
  4. Save as instagram_cookies.txt in this folder

USAGE:
  python reel2script.py
  python reel2script.py https://www.instagram.com/reel/XXXXX/

MORE TOOLS: github.com/YOUR_USERNAME/2script-toolkit
"""

import sys
import os
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

# ── Auto-install dependencies ────────────────────────────────────────────────
def ensure_dependencies():
    missing = []
    try:
        import yt_dlp
    except ImportError:
        missing.append("yt-dlp")
    try:
        import whisper
    except ImportError:
        missing.append("openai-whisper")
    if missing:
        print(f"📦 Installing: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing, "-q"])
        print("✅ Done. Re-run the script.\n")
        sys.exit(0)

ensure_dependencies()

import yt_dlp
import whisper

# ── Config ───────────────────────────────────────────────────────────────────
WHISPER_MODEL = "base"
OUTPUT_DIR = Path.home() / "StealList"
OUTPUT_DIR.mkdir(exist_ok=True)

# Cookies file — must be in the same folder as this script
COOKIES_FILE = Path(__file__).parent / "instagram_cookies.txt"

# ── Core functions ────────────────────────────────────────────────────────────
def download_audio(url: str, tmpdir: str):
    print("⬇️  Downloading reel audio...")

    if not COOKIES_FILE.exists():
        raise FileNotFoundError(
            f"Cookies file not found at: {COOKIES_FILE}\n\n"
            "To fix this:\n"
            "  1. Install 'Get cookies.txt LOCALLY' extension in Chrome\n"
            "  2. Go to instagram.com (while logged in)\n"
            "  3. Click the extension → select instagram.com → Export\n"
            "  4. Save the file as 'instagram_cookies.txt' in this folder:\n"
            f"     {COOKIES_FILE.parent}"
        )

    audio_path = os.path.join(tmpdir, "reel.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": audio_path,
        "quiet": True,
        "no_warnings": True,
        "cookiefile": str(COOKIES_FILE),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "128",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "untitled")[:60]

    mp3_path = os.path.join(tmpdir, "reel.mp3")
    return mp3_path, title


def transcribe(audio_path: str) -> str:
    print(f"🎙️  Transcribing with Whisper ({WHISPER_MODEL} model)...")
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(audio_path, fp16=False)
    return result["text"].strip()


def save_transcript(transcript: str, title: str, url: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
    filename = OUTPUT_DIR / f"{timestamp}_{safe_title[:40]}.txt"
    content = f"""SOURCE: {url}
TITLE: {title}
DATE: {datetime.now().strftime("%Y-%m-%d %H:%M")}
{'─' * 60}

{transcript}

{'─' * 60}
[Transcribed by reel_to_script.py using OpenAI Whisper]
"""
    filename.write_text(content, encoding="utf-8")
    return filename


def print_transcript(transcript: str, title: str):
    width = 60
    print("\n" + "═" * width)
    print(f"📄  TRANSCRIPT: {title[:50]}")
    print("═" * width)
    print()
    print(transcript)
    print()
    print("═" * width)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
    else:
        print("🎬  Instagram Reel → Script Extractor")
        print("──────────────────────────────────────")
        url = input("Paste Instagram URL: ").strip()

    if not url:
        print("❌ No URL provided.")
        sys.exit(1)

    url = url.split("?")[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            audio_path, title = download_audio(url, tmpdir)
            transcript = transcribe(audio_path)
        except FileNotFoundError as e:
            print(f"\n❌ {e}")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\n💡 Tips:")
            print("  - Re-export instagram_cookies.txt (cookies expire over time)")
            print("  - Make sure the reel is public")
            print("  - Update yt-dlp: pip install -U yt-dlp")
            sys.exit(1)

    print_transcript(transcript, title)
    saved_path = save_transcript(transcript, title, url)
    print(f"✅ Saved to: {saved_path}")
    print(f"\n📋 Copy the script above and paste into Notion!")

    try:
        import pyperclip
        pyperclip.copy(transcript)
        print("📋 Also copied to clipboard automatically!")
    except ImportError:
        pass


if __name__ == "__main__":
    main()
