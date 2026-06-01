# ⚡ GroqTranslate

macOS menu bar translator powered by Groq AI. Translate anything on your screen with a keyboard shortcut.

## Features

- **⌘K** — OCR: select a screen region, extract and translate text
- **⌘C ⌘C** (double tap) — translate selected/clipboard text
- 20+ languages with auto-detection
- Translation history (local SQLite)
- Your own Groq API key — free, no server limits
- Native macOS menu bar app

## Download

👉 [preklad.alukim.sk](https://preklad.alukim.sk)

## Requirements

- macOS 12 Monterey or later
- Python 3.10+
- Groq API key (free at [console.groq.com](https://console.groq.com/keys))

## Install from source

```bash
cd app
pip3 install -r requirements.txt
python3 main.py
```

## Build .app bundle

```bash
cd app
chmod +x build.sh
./build.sh
```

## Groq Free Tier

- 14,400 requests/day
- 30 requests/minute
- Models: Llama 3.3 70B, Mixtral

More than enough for personal translation use.

## Permissions needed

- **Accessibility** — for global keyboard shortcuts
- **Screen Recording** — for OCR (screenshot capture)

## License

MIT — free to use, modify, distribute.
