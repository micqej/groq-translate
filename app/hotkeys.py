"""
Global hotkeys via macOS CGEventTap (Quartz).
  ⌘K       → OCR
  ⌘C ⌘C   → translate clipboard (double tap within 0.5s)
"""

import threading
import time


class HotkeyManager:
    def __init__(self, on_ocr, on_clipboard):
        self.on_ocr = on_ocr
        self.on_clipboard = on_clipboard
        self._last_c = 0.0

    def start(self):
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self):
        try:
            import Quartz
            import CoreFoundation

            KEY_C = 8
            KEY_K = 40
            CMD = Quartz.kCGEventFlagMaskCommand

            def handler(proxy, etype, event, _):
                try:
                    if etype == Quartz.kCGEventKeyDown:
                        flags = Quartz.CGEventGetFlags(event)
                        key = Quartz.CGEventGetIntegerValueField(
                            event, Quartz.kCGKeyboardEventKeycode
                        )
                        if flags & CMD:
                            if key == KEY_K:
                                threading.Thread(target=self.on_ocr, daemon=True).start()
                            elif key == KEY_C:
                                now = time.time()
                                if now - self._last_c < 0.5:
                                    threading.Thread(target=self.on_clipboard, daemon=True).start()
                                    self._last_c = 0
                                else:
                                    self._last_c = now
                except Exception:
                    pass
                return event

            mask = 1 << Quartz.kCGEventKeyDown
            tap = Quartz.CGEventTapCreate(
                Quartz.kCGSessionEventTap,
                Quartz.kCGHeadInsertEventTap,
                0,
                mask,
                handler,
                None,
            )

            if tap is None:
                return  # No accessibility — app still works via menu

            src = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
            loop = CoreFoundation.CFRunLoopGetCurrent()
            CoreFoundation.CFRunLoopAddSource(
                loop, src, CoreFoundation.kCFRunLoopCommonModes
            )
            Quartz.CGEventTapEnable(tap, True)
            CoreFoundation.CFRunLoopRun()

        except Exception:
            pass  # Hotkeys unavailable but app still works
