"""
Global hotkeys via macOS Quartz CGEventTap (no pynput).
  CMD+K       → OCR
  Double CMD+C → translate clipboard
"""

import threading
import time
import ctypes
import objc
from Quartz import (
    CGEventTapCreate,
    CGEventTapEnable,
    CFMachPortCreateRunLoopSource,
    CFRunLoopAddSource,
    CFRunLoopGetCurrent,
    CFRunLoopRun,
    kCGSessionEventTap,
    kCGHeadInsertEventTap,
    kCGEventFlagMaskCommand,
    kCGEventKeyDown,
    CGEventGetIntegerValueField,
    CGEventGetFlags,
    kCGKeyboardEventKeycode,
)
import CoreFoundation

# macOS keycodes
KEY_C = 8
KEY_K = 40


class HotkeyManager:
    def __init__(self, on_ocr, on_clipboard):
        self.on_ocr = on_ocr
        self.on_clipboard = on_clipboard
        self._last_c_time = 0.0
        self._thread = None

    def start(self):
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self):
        def callback(proxy, event_type, event, refcon):
            try:
                if event_type == kCGEventKeyDown:
                    flags = CGEventGetFlags(event)
                    cmd = bool(flags & kCGEventFlagMaskCommand)
                    keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)

                    if cmd and keycode == KEY_K:
                        threading.Thread(target=self.on_ocr, daemon=True).start()

                    elif cmd and keycode == KEY_C:
                        now = time.time()
                        if now - self._last_c_time < 0.45:
                            threading.Thread(target=self.on_clipboard, daemon=True).start()
                            self._last_c_time = 0
                        else:
                            self._last_c_time = now
            except Exception:
                pass
            return event

        tap = CGEventTapCreate(
            kCGSessionEventTap,
            kCGHeadInsertEventTap,
            0,
            (1 << kCGEventKeyDown),
            callback,
            None,
        )

        if tap is None:
            # No accessibility permission — hotkeys won't work but app still runs
            return

        source = CFMachPortCreateRunLoopSource(None, tap, 0)
        CFRunLoopAddSource(CFRunLoopGetCurrent(), source, CoreFoundation.kCFRunLoopCommonModes)
        CGEventTapEnable(tap, True)
        CFRunLoopRun()
