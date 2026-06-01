#!/usr/bin/env python3
"""
Prekladač — macOS menu bar translator
"""

import rumps
import threading
import json
import os
import subprocess
from translator import translate_text
from ocr import capture_and_ocr
from database import HistoryDB
from hotkeys import HotkeyManager

CONFIG_PATH = os.path.expanduser("~/.config/prekladac/config.json")
ICON_PATH = os.path.join(os.path.dirname(__file__), "menubar_icon.png")

DEFAULT_CONFIG = {
    "api_key": "",
    "source_lang": "auto",
    "target_lang": "sk",
}

LANGUAGES = {
    "auto": "Automaticky",
    "sk": "Slovenčina",
    "cs": "Čeština",
    "en": "Angličtina",
    "de": "Nemčina",
    "fr": "Francúzština",
    "es": "Španielčina",
    "it": "Taliančina",
    "pl": "Poľština",
    "hu": "Maďarčina",
    "ru": "Ruština",
    "zh": "Čínština",
    "ja": "Japončina",
    "ko": "Kórejčina",
    "uk": "Ukrajinčina",
}


def notify(title, message):
    """Show macOS notification."""
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script], capture_output=True)


def ask(prompt, default=""):
    """Show input dialog via AppleScript."""
    script = f'display dialog "{prompt}" default answer "{default}" with title "Prekladač"'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip().split("text returned:")[-1].strip()
    return None


def show_result(original, translated):
    """Show translation result — copy to clipboard option."""
    short = translated[:200] + ("..." if len(translated) > 200 else "")
    script = f'''
    set r to display dialog "Preklad:" & return & return & "{short}" ¬
        with title "Prekladač" ¬
        buttons {{"Zavrieť", "Kopírovať"}} ¬
        default button "Kopírovať"
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if "Kopírovať" in result.stdout:
        subprocess.run(["pbcopy"], input=translated.encode())


class PrekladacApp(rumps.App):
    def __init__(self):
        icon = ICON_PATH if os.path.exists(ICON_PATH) else None
        super().__init__(
            "Prekladač",
            icon=icon,
            template=True,
            quit_button=None,
        )
        self.config = self._load_config()
        self.db = HistoryDB()
        self._build_menu()
        self.hotkeys = HotkeyManager(
            on_ocr=self._trigger_ocr,
            on_clipboard=self._trigger_clipboard,
        )
        self.hotkeys.start()

    def _load_config(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH) as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except Exception:
                pass
        return DEFAULT_CONFIG.copy()

    def save_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=2)

    def _build_menu(self):
        tgt = LANGUAGES.get(self.config["target_lang"], "?")
        src = LANGUAGES.get(self.config["source_lang"], "Auto")

        source_items = [
            rumps.MenuItem(
                ("✓ " if code == self.config["source_lang"] else "  ") + name,
                callback=lambda _, c=code: self._set_source(c),
            )
            for code, name in LANGUAGES.items()
        ]
        target_items = [
            rumps.MenuItem(
                ("✓ " if code == self.config["target_lang"] else "  ") + name,
                callback=lambda _, c=code: self._set_target(c),
            )
            for code, name in LANGUAGES.items()
            if code != "auto"
        ]

        self.menu = [
            rumps.MenuItem(f"{src} → {tgt}"),
            None,
            rumps.MenuItem("⌘K  OCR — vyber oblasť", callback=self._trigger_ocr),
            rumps.MenuItem("2×C  Preložiť výber", callback=self._trigger_clipboard),
            None,
            rumps.MenuItem("Zdrojový jazyk", source_items),
            rumps.MenuItem("Cieľový jazyk", target_items),
            None,
            rumps.MenuItem("🔑  Nastaviť API kľúč", callback=self._set_api_key),
            rumps.MenuItem("📋  História (posledných 5)", callback=self._show_history),
            None,
            rumps.MenuItem("Ukončiť", callback=rumps.quit_application),
        ]

    def _set_source(self, code):
        self.config["source_lang"] = code
        self.save_config()
        self._build_menu()

    def _set_target(self, code):
        self.config["target_lang"] = code
        self.save_config()
        self._build_menu()

    @rumps.clicked("🔑  Nastaviť API kľúč")
    def _set_api_key(self, _=None):
        current = self.config.get("api_key", "")
        hint = current[:8] + "..." if len(current) > 8 else ""
        val = ask(f"Vlož Groq API kľúč:\n(aktuálny: {hint or 'nenastavený'})\n\nconsole.groq.com → API Keys")
        if val and val.strip():
            self.config["api_key"] = val.strip()
            self.save_config()
            notify("Prekladač", "API kľúč bol uložený ✓")

    def _trigger_ocr(self, _=None):
        if not self.config.get("api_key"):
            notify("Prekladač", "⚠️ Najprv nastav API kľúč — klikni na ikonku → Nastaviť API kľúč")
            return
        threading.Thread(target=self._do_ocr, daemon=True).start()

    def _do_ocr(self):
        notify("Prekladač", "🔍 Vyber oblasť na obrazovke...")
        text = capture_and_ocr()
        if not text or not text.strip():
            notify("Prekladač", "❌ Žiadny text sa nenašiel")
            return
        notify("Prekladač", "⏳ Prekladám...")
        result = translate_text(
            text, self.config["source_lang"], self.config["target_lang"], self.config["api_key"]
        )
        if result:
            self.db.add(text, result, self.config["source_lang"], self.config["target_lang"])
            threading.Thread(target=show_result, args=(text, result), daemon=True).start()

    def _trigger_clipboard(self, _=None):
        if not self.config.get("api_key"):
            notify("Prekladač", "⚠️ Najprv nastav API kľúč")
            return
        threading.Thread(target=self._do_clipboard, daemon=True).start()

    def _do_clipboard(self):
        r = subprocess.run(["pbpaste"], capture_output=True, text=True)
        text = r.stdout.strip()
        if not text:
            notify("Prekladač", "❌ Schránka je prázdna — skopíruj najprv nejaký text")
            return
        notify("Prekladač", "⏳ Prekladám...")
        result = translate_text(
            text, self.config["source_lang"], self.config["target_lang"], self.config["api_key"]
        )
        if result:
            self.db.add(text, result, self.config["source_lang"], self.config["target_lang"])
            threading.Thread(target=show_result, args=(text, result), daemon=True).start()

    def _show_history(self, _=None):
        rows = self.db.get_all(limit=5)
        if not rows:
            notify("Prekladač", "História je prázdna")
            return
        lines = []
        for row in rows:
            _, src, tgt, *_ = row
            lines.append(f"• {src[:40]}…\n  → {tgt[:40]}…")
        text = "\n\n".join(lines)
        subprocess.run(
            ["osascript", "-e", f'display dialog "{text}" with title "Posledné preklady" buttons {{"OK"}}'],
            capture_output=True,
        )


if __name__ == "__main__":
    app = PrekladacApp()
    app.run()
