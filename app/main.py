#!/usr/bin/env python3
"""Prekladac — macOS menu bar translator"""

import rumps
import threading
import json
import os
import subprocess
from translator import translate_text
from ocr import capture_and_ocr
from database import HistoryDB
from hotkeys import HotkeyManager
from floating import show_result, show_status

CONFIG_PATH = os.path.expanduser("~/.config/prekladac/config.json")
ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "menubar_icon.png")

DEFAULT_CONFIG = {
    "api_key": "",
    "source_lang": "auto",
    "target_lang": "sk",
}

LANGUAGES = {
    "auto": "Automaticky",
    "sk": "Slovenčina", "cs": "Čeština", "en": "Angličtina",
    "de": "Nemčina", "fr": "Francúzština", "es": "Španielčina",
    "it": "Taliančina", "pl": "Poľština", "hu": "Maďarčina",
    "ru": "Ruština", "uk": "Ukrajinčina", "zh": "Čínština",
    "ja": "Japončina", "ko": "Kórejčina",
}


class PrekladacApp(rumps.App):
    def __init__(self):
        icon = ICON_PATH if os.path.exists(ICON_PATH) else None
        super().__init__("", icon=icon, template=True, quit_button=None)
        self.config = self._load_config()
        self.db = HistoryDB()
        self._build_menu()
        HotkeyManager(on_ocr=self._do_ocr, on_clipboard=self._do_clipboard).start()

    def _load_config(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        try:
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH) as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            pass
        return DEFAULT_CONFIG.copy()

    def save_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=2)

    def _build_menu(self):
        src_name = LANGUAGES.get(self.config["source_lang"], "?")
        tgt_name = LANGUAGES.get(self.config["target_lang"], "?")

        src_items = [
            rumps.MenuItem(
                ("✓ " if code == self.config["source_lang"] else "   ") + name,
                callback=lambda _, c=code: self._set_lang("source_lang", c),
            )
            for code, name in LANGUAGES.items()
        ]
        tgt_items = [
            rumps.MenuItem(
                ("✓ " if code == self.config["target_lang"] else "   ") + name,
                callback=lambda _, c=code: self._set_lang("target_lang", c),
            )
            for code, name in LANGUAGES.items()
            if code != "auto"
        ]

        has_key = bool(self.config.get("api_key"))
        key_status = "✓ API kľúč nastavený" if has_key else "⚠️  Nastav API kľúč"

        self.menu = [
            rumps.MenuItem(f"{src_name} → {tgt_name}"),
            None,
            rumps.MenuItem("Preložiť výber  (⌘C ⌘C)", callback=lambda _: threading.Thread(target=self._do_clipboard, daemon=True).start()),
            rumps.MenuItem("OCR snímka  (⌘K)", callback=lambda _: threading.Thread(target=self._do_ocr, daemon=True).start()),
            None,
            rumps.MenuItem("Zdrojový jazyk", src_items),
            rumps.MenuItem("Cieľový jazyk", tgt_items),
            None,
            rumps.MenuItem(key_status, callback=self._set_api_key),
            None,
            rumps.MenuItem("Ukončiť", callback=rumps.quit_application),
        ]

    def _set_lang(self, key, code):
        self.config[key] = code
        self.save_config()
        self._build_menu()

    def _set_api_key(self, _=None):
        current = self.config.get("api_key", "")
        hint = (current[:6] + "…") if current else "prázdny"
        result = subprocess.run(
            ["osascript", "-e",
             f'display dialog "Vlož Groq API kľúč:\\n(aktuálny: {hint})\\n\\nZískaš zadarmo na console.groq.com" '
             f'default answer "" with title "Prekladač — API kľúč"'],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            val = result.stdout.strip().split("text returned:")[-1].strip()
            if val:
                self.config["api_key"] = val
                self.save_config()
                self._build_menu()
                show_status("API kľúč uložený ✓")

    def _do_clipboard(self):
        if not self.config.get("api_key"):
            show_status("⚠️ Nastav API kľúč — klikni na ikonku v menu bare")
            return
        r = subprocess.run(["pbpaste"], capture_output=True, text=True)
        text = r.stdout.strip()
        if not text:
            show_status("Schránka je prázdna — skopíruj najprv text")
            return
        show_status("Prekladám…")
        result = translate_text(text, self.config["source_lang"], self.config["target_lang"], self.config["api_key"])
        if result and not result.startswith("Chyba:"):
            self.db.add(text, result, self.config["source_lang"], self.config["target_lang"])
            show_result(text, result)
        else:
            show_status(result or "Chyba prekladu")

    def _do_ocr(self):
        if not self.config.get("api_key"):
            show_status("⚠️ Nastav API kľúč — klikni na ikonku v menu bare")
            return
        show_status("Vyber oblasť na obrazovke…")
        text = capture_and_ocr()
        if not text or not text.strip():
            show_status("Žiadny text sa nenašiel")
            return
        show_status("Prekladám…")
        result = translate_text(text, self.config["source_lang"], self.config["target_lang"], self.config["api_key"])
        if result and not result.startswith("Chyba:"):
            self.db.add(text, result, self.config["source_lang"], self.config["target_lang"])
            show_result(text, result)
        else:
            show_status(result or "Chyba prekladu")


if __name__ == "__main__":
    PrekladacApp().run()
