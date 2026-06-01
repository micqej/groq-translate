"""
Global hotkey listener:
  - CMD+K       → OCR capture & translate
  - double CMD+C → translate clipboard content
"""

import threading
import time
from pynput import keyboard


class HotkeyManager:
    def __init__(self, on_ocr, on_clipboard):
        self.on_ocr = on_ocr
        self.on_clipboard = on_clipboard
        self._last_c_time = 0.0
        self._double_tap_threshold = 0.4  # seconds
        self._listener = None
        self._pressed = set()

    def start(self):
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        self._listener.daemon = True
        self._listener.start()

    def stop(self):
        if self._listener:
            self._listener.stop()

    def _on_press(self, key):
        self._pressed.add(key)

        # CMD+K → OCR
        cmd_pressed = (
            keyboard.Key.cmd in self._pressed
            or keyboard.Key.cmd_l in self._pressed
            or keyboard.Key.cmd_r in self._pressed
        )

        if cmd_pressed:
            try:
                if key.char == "k":
                    threading.Thread(target=self.on_ocr, daemon=True).start()
                    return
            except AttributeError:
                pass

        # Double CMD+C → clipboard translate
        if cmd_pressed:
            try:
                if key.char == "c":
                    now = time.time()
                    if now - self._last_c_time < self._double_tap_threshold:
                        threading.Thread(target=self.on_clipboard, daemon=True).start()
                        self._last_c_time = 0.0
                    else:
                        self._last_c_time = now
            except AttributeError:
                pass

    def _on_release(self, key):
        self._pressed.discard(key)
