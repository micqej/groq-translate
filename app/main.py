#!/usr/bin/env python3
"""
GroqTranslate - macOS menu bar translation app
Uses Groq API for fast AI translation + macOS Vision for OCR
"""

import rumps
import threading
import json
import os
from translator import translate_text
from ocr import capture_and_ocr
from database import HistoryDB
from hotkeys import HotkeyManager
from ui import FloatingWindow, SettingsWindow

CONFIG_PATH = os.path.expanduser("~/.config/groq-translator/config.json")
DEFAULT_CONFIG = {
    "api_key": "",
    "source_lang": "auto",
    "target_lang": "sk",
    "theme_color": "#6366f1",
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
    "uk": "Ukrajinčina",
    "ru": "Ruština",
    "zh": "Čínština",
    "ja": "Japončina",
    "ko": "Kórejčina",
    "pt": "Portugalčina",
    "nl": "Holandčina",
    "tr": "Turečtina",
    "ar": "Arabčina",
}


class GroqTranslateApp(rumps.App):
    def __init__(self):
        super().__init__(
            "GroqTranslate",
            icon=None,
            template=True,
            quit_button=None,
        )
        self.config = self._load_config()
        self.db = HistoryDB()
        self.floating = FloatingWindow(self)
        self._build_menu()
        self.hotkeys = HotkeyManager(
            on_ocr=self._trigger_ocr,
            on_clipboard=self._trigger_clipboard,
        )
        self.hotkeys.start()

    def _load_config(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                cfg = json.load(f)
                # merge with defaults for new keys
                return {**DEFAULT_CONFIG, **cfg}
        return DEFAULT_CONFIG.copy()

    def save_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=2)

    def _build_menu(self):
        self.menu.clear()
        target = self.config["target_lang"]

        # Source language submenu
        source_items = []
        for code, name in LANGUAGES.items():
            item = rumps.MenuItem(
                f"{'✓ ' if code == self.config['source_lang'] else '   '}{name}",
                callback=lambda s, c=code: self._set_source(c),
            )
            source_items.append(item)

        # Target language submenu
        target_items = []
        for code, name in {k: v for k, v in LANGUAGES.items() if k != "auto"}.items():
            item = rumps.MenuItem(
                f"{'✓ ' if code == target else '   '}{name}",
                callback=lambda s, c=code: self._set_target(c),
            )
            target_items.append(item)

        src_name = LANGUAGES.get(self.config["source_lang"], "Auto")
        tgt_name = LANGUAGES.get(target, target)

        self.menu = [
            rumps.MenuItem(f"Preložiť: {src_name} → {tgt_name}"),
            None,
            rumps.MenuItem("⌘K  OCR Prekladač", callback=self._trigger_ocr),
            rumps.MenuItem("2×C  Preložiť výber", callback=self._trigger_clipboard),
            None,
            rumps.MenuItem("Zdrojový jazyk", [*source_items]),
            rumps.MenuItem("Cieľový jazyk", [*target_items]),
            None,
            rumps.MenuItem("📋 História prekladov", callback=self._show_history),
            rumps.MenuItem("⚙️  Nastavenia", callback=self._show_settings),
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

    def _trigger_ocr(self, _=None):
        if not self.config.get("api_key"):
            self.floating.show("⚠️ Nastav Groq API kľúč v Nastaveniach", "")
            return
        threading.Thread(target=self._do_ocr, daemon=True).start()

    def _do_ocr(self):
        self.floating.show("🔍 Zachytávam obrazovku...", "")
        text = capture_and_ocr()
        if not text or not text.strip():
            self.floating.show("❌ Žiadny text nenájdený", "")
            return
        self.floating.show(f"📝 {text[:80]}...", "Prekladám...")
        result = translate_text(
            text, self.config["source_lang"], self.config["target_lang"], self.config["api_key"]
        )
        if result:
            self.floating.show(text, result)
            self.db.add(text, result, self.config["source_lang"], self.config["target_lang"])

    def _trigger_clipboard(self, _=None):
        if not self.config.get("api_key"):
            self.floating.show("⚠️ Nastav Groq API kľúč v Nastaveniach", "")
            return
        threading.Thread(target=self._do_clipboard, daemon=True).start()

    def _do_clipboard(self):
        import subprocess
        result = subprocess.run(["pbpaste"], capture_output=True, text=True)
        text = result.stdout.strip()
        if not text:
            self.floating.show("❌ Schránka je prázdna", "")
            return
        self.floating.show(f"📝 {text[:80]}...", "Prekladám...")
        translated = translate_text(
            text, self.config["source_lang"], self.config["target_lang"], self.config["api_key"]
        )
        if translated:
            self.floating.show(text, translated)
            self.db.add(text, translated, self.config["source_lang"], self.config["target_lang"])

    def _show_history(self, _=None):
        from ui import HistoryWindow
        HistoryWindow(self.db).run()

    def _show_settings(self, _=None):
        SettingsWindow(self).run()


if __name__ == "__main__":
    app = GroqTranslateApp()
    app.run()
