# 2script-toolkit

> Turn any content format into a clean, editable script.

A growing collection of free, open-source tools for content creators who are tired of manually transcribing videos, reels, and carousels. Paste a URL. Get a script. Remix it as your own.

**100% free · Runs locally · No API keys · No subscriptions · No BS**

---

## The Lineup

| Tool | Status | What it does |
|---|---|---|
| 🟢 **reel2script** | Available now | Instagram Reels → transcript |
| 🔜 **shorts2script** | Coming soon | YouTube Shorts → transcript |
| 🔜 **carousel2script** | Coming soon | Instagram Carousels → text dump |
| 🔜 **clip2script** | Coming soon | TikTok videos → transcript |
| 🔜 **pod2script** | Coming soon | Podcast episodes → transcript |

Each tool is a single Python script. No installation wizard. No Electron app. Just drop it in a folder and run it.

---

## reel2script

The first tool in the toolkit. Paste an Instagram reel URL → get a clean transcript in ~30 seconds.

### How it works

1. Downloads the reel audio using your Instagram login session
2. Runs it through [OpenAI Whisper](https://github.com/openai/whisper) — locally, on your machine
3. Prints the transcript to your terminal, copies it to clipboard, and saves a `.txt` file to `~/StealList/`

---

### Requirements

- Python 3.8+
- ffmpeg
- Google Chrome (for the one-time cookie export)

---

### Setup

#### Step 1 — Install ffmpeg

**Windows:**
1. Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) → Windows builds by BtbN
2. Extract the zip → open the `bin` folder inside
3. Copy the full path to that `bin` folder
4. Search "Environment Variables" in Windows → Edit System Variables → Path → New → paste the path
5. Reopen your terminal and verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

---

#### Step 2 — Install Python packages

```bash
pip install yt-dlp openai-whisper pyperclip
```

> First run will download the Whisper `base` model (~140MB). One-time only. Every run after is fast.

---

#### Step 3 — Export your Instagram cookies (one-time)

Instagram requires you to be logged in to download reels. The script handles this by reading a cookies file — your password is never stored, just your session.

1. Install **[Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)** in Chrome
2. Go to [instagram.com](https://instagram.com) while logged in
3. Click the extension icon → select `instagram.com` → click **Export**
4. Save the file as `instagram_cookies.txt` in the same folder as `reel2script.py`

```
2script-toolkit/
  ├── reel2script.py
  ├── instagram_cookies.txt   ← your cookies file (never committed to git)
  └── requirements.txt
```

> ⚠️ Cookies expire after a few weeks. If downloads start failing, just re-export from Chrome using the same steps.

---

### Usage

```bash
# Interactive — paste URL when prompted
python reel2script.py

# Or pass the URL directly
python reel2script.py https://www.instagram.com/reel/XXXXX/
```

That's it. Your transcript will print in the terminal, copy to clipboard automatically, and save to `~/StealList/` with a timestamp.

---

### Configuration

Open `reel2script.py` and tweak the config block near the top:

```python
WHISPER_MODEL = "base"   # Options: tiny · base · small · medium · large
OUTPUT_DIR = Path.home() / "StealList"   # Change this to wherever you want
```

**Whisper model guide:**

| Model | Speed | Accuracy | Best for |
|---|---|---|---|
| tiny | Fastest | Lower | Quick drafts, short clips |
| base | Fast | Good | Most reels ✅ default |
| small | Medium | Better | Heavy accents, background music |
| medium | Slow | Great | When accuracy really matters |

---

### Troubleshooting

| Problem | Fix |
|---|---|
| `ffmpeg not found` | Re-check PATH setup and reopen terminal |
| `cookies file not found` | Re-export `instagram_cookies.txt` to the same folder |
| Download fails / 401 error | Cookies expired — re-export from Chrome |
| Whisper taking too long | Switch to `WHISPER_MODEL = "tiny"` in the script |
| Private reel fails | Only public posts are supported |

---

## My workflow (why I built this)

I save reels I want to steal ideas from. My Instagram collection was overflowing and I never did anything with it — the manual transcription step killed the momentum every time.

This script kills that friction. Now my workflow is:

1. Save reel to Instagram "Steal List" collection
2. Run `reel2script.py` → transcript in `~/StealList/`
3. Drop into Notion → rewrite in my own voice
4. Post

The full story is in this blog post: [I Built a Tool That Turns Instagram Reels Into Scripts](https://fattahia.com/blog)

---

## Contributing

This is a fun, free, personal project — but PRs and ideas are welcome. If you build a `shorts2script` or `carousel2script` variant, open a PR and let's add it to the lineup.

---

## License

MIT — use it, fork it, build on it, sell it if you want. Just keep it honest.

---

Built with curiosity by [Nafim](https://fattahia.com) · [Nartz Web Studio](https://nartz.com) · [@fattahia.design](https://instagram.com/fattahia.design)
