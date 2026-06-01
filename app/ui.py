"""
UI components: FloatingWindow, SettingsWindow, HistoryWindow
Uses tkinter (built-in Python, no extra install)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess


ACCENT = "#6366f1"
BG_DARK = "#1e1e2e"
BG_CARD = "#2a2a3e"
TEXT_PRIMARY = "#e2e8f0"
TEXT_SECONDARY = "#94a3b8"
SUCCESS = "#10b981"
ERROR = "#ef4444"


def _apply_dark_style(root):
    root.configure(bg=BG_DARK)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(".", background=BG_DARK, foreground=TEXT_PRIMARY, font=("SF Pro Display", 13))
    style.configure("TButton", background=ACCENT, foreground="white", borderwidth=0, padding=8)
    style.map("TButton", background=[("active", "#4f52d4")])
    style.configure("TEntry", fieldbackground=BG_CARD, foreground=TEXT_PRIMARY, borderwidth=1)
    style.configure("TLabel", background=BG_DARK, foreground=TEXT_PRIMARY)


class FloatingWindow:
    """Small floating result window that appears near cursor."""

    def __init__(self, app):
        self.app = app
        self._win = None
        self._lock = threading.Lock()

    def show(self, source: str, translation: str):
        import rumps
        # Run on main thread via rumps timer trick
        threading.Thread(target=self._show_tk, args=(source, translation), daemon=True).start()

    def _show_tk(self, source: str, translation: str):
        with self._lock:
            if self._win:
                try:
                    self._win.destroy()
                except Exception:
                    pass

            win = tk.Tk()
            win.title("")
            win.overrideredirect(True)
            win.attributes("-topmost", True)
            win.attributes("-alpha", 0.95)
            win.configure(bg=BG_DARK)

            # Position near top-right
            w, h = 420, 180
            sw = win.winfo_screenwidth()
            x = sw - w - 20
            y = 50
            win.geometry(f"{w}x{h}+{x}+{y}")

            # Header bar
            header = tk.Frame(win, bg=ACCENT, height=4)
            header.pack(fill="x")

            content = tk.Frame(win, bg=BG_DARK, padx=16, pady=12)
            content.pack(fill="both", expand=True)

            if translation and translation != source:
                src_label = tk.Label(
                    content, text=source[:120] + ("..." if len(source) > 120 else ""),
                    bg=BG_DARK, fg=TEXT_SECONDARY, font=("SF Pro Display", 11),
                    wraplength=380, justify="left", anchor="w"
                )
                src_label.pack(fill="x", pady=(0, 6))

                sep = tk.Frame(content, bg=BG_CARD, height=1)
                sep.pack(fill="x", pady=4)

                trans_label = tk.Label(
                    content, text=translation[:200] + ("..." if len(translation) > 200 else ""),
                    bg=BG_DARK, fg=TEXT_PRIMARY, font=("SF Pro Display", 13, "bold"),
                    wraplength=380, justify="left", anchor="w"
                )
                trans_label.pack(fill="x", pady=(4, 0))
            else:
                # Status message
                msg_label = tk.Label(
                    content, text=source,
                    bg=BG_DARK, fg=TEXT_PRIMARY, font=("SF Pro Display", 13),
                    wraplength=380, justify="left", anchor="w"
                )
                msg_label.pack(fill="both", expand=True)

            # Buttons row
            btn_frame = tk.Frame(content, bg=BG_DARK)
            btn_frame.pack(fill="x", pady=(8, 0))

            if translation and not translation.startswith("❌"):
                copy_btn = tk.Button(
                    btn_frame, text="Kopírovať",
                    bg=ACCENT, fg="white", relief="flat",
                    font=("SF Pro Display", 11), padx=12, pady=4,
                    cursor="hand2",
                    command=lambda: [
                        subprocess.run(["pbcopy"], input=translation.encode()),
                        win.destroy()
                    ]
                )
                copy_btn.pack(side="left")

            close_btn = tk.Button(
                btn_frame, text="✕",
                bg=BG_CARD, fg=TEXT_SECONDARY, relief="flat",
                font=("SF Pro Display", 11), padx=12, pady=4,
                cursor="hand2",
                command=win.destroy
            )
            close_btn.pack(side="right")

            self._win = win
            # Auto-close after 8 seconds
            win.after(8000, lambda: win.destroy() if win.winfo_exists() else None)
            win.mainloop()


class SettingsWindow:
    """Settings popup: API key, languages."""

    def __init__(self, app):
        self.app = app

    def run(self):
        win = tk.Tk()
        win.title("GroqTranslate — Nastavenia")
        win.geometry("480x320")
        win.resizable(False, False)
        _apply_dark_style(win)

        # Header
        tk.Label(win, text="⚙️  Nastavenia", font=("SF Pro Display", 18, "bold"),
                 bg=BG_DARK, fg=TEXT_PRIMARY).pack(pady=(24, 4))
        tk.Label(win, text="Nakonfiguruj si GroqTranslate", font=("SF Pro Display", 12),
                 bg=BG_DARK, fg=TEXT_SECONDARY).pack(pady=(0, 20))

        form = tk.Frame(win, bg=BG_DARK, padx=32)
        form.pack(fill="x")

        # API Key
        tk.Label(form, text="Groq API kľúč", bg=BG_DARK, fg=TEXT_SECONDARY,
                 font=("SF Pro Display", 11)).grid(row=0, column=0, sticky="w", pady=4)
        api_var = tk.StringVar(value=self.app.config.get("api_key", ""))
        api_entry = tk.Entry(form, textvariable=api_var, width=36, show="•",
                             bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                             relief="flat", font=("SF Pro Display", 12))
        api_entry.grid(row=0, column=1, padx=(12, 0), pady=4, sticky="ew")

        show_var = tk.BooleanVar()
        def toggle_show():
            api_entry.config(show="" if show_var.get() else "•")
        tk.Checkbutton(form, text="Zobraziť", variable=show_var, command=toggle_show,
                       bg=BG_DARK, fg=TEXT_SECONDARY, selectcolor=BG_CARD,
                       activebackground=BG_DARK, font=("SF Pro Display", 10)).grid(row=1, column=1, sticky="w", padx=12)

        # Get API key link
        tk.Label(form, text="Získaj zadarmo: console.groq.com",
                 bg=BG_DARK, fg=ACCENT, font=("SF Pro Display", 10),
                 cursor="hand2").grid(row=2, column=1, sticky="w", padx=12, pady=(0, 16))

        # Save button
        def save():
            self.app.config["api_key"] = api_var.get().strip()
            self.app.save_config()
            messagebox.showinfo("Uložené", "Nastavenia boli uložené!", parent=win)
            win.destroy()

        btn = tk.Button(win, text="Uložiť nastavenia",
                        bg=ACCENT, fg="white", relief="flat",
                        font=("SF Pro Display", 13, "bold"), padx=24, pady=10,
                        cursor="hand2", command=save)
        btn.pack(pady=20)

        win.mainloop()


class HistoryWindow:
    """Translation history browser."""

    def __init__(self, db):
        self.db = db

    def run(self):
        win = tk.Tk()
        win.title("GroqTranslate — História prekladov")
        win.geometry("720x520")
        _apply_dark_style(win)

        # Header
        header = tk.Frame(win, bg=BG_DARK, padx=20, pady=16)
        header.pack(fill="x")

        tk.Label(header, text="📋 História prekladov",
                 font=("SF Pro Display", 18, "bold"), bg=BG_DARK, fg=TEXT_PRIMARY).pack(side="left")

        # Search
        search_var = tk.StringVar()
        search_entry = tk.Entry(header, textvariable=search_var, width=24,
                                bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                                relief="flat", font=("SF Pro Display", 12))
        search_entry.pack(side="right", padx=(0, 8))
        tk.Label(header, text="🔍", bg=BG_DARK, fg=TEXT_SECONDARY).pack(side="right")

        # Table
        cols = ("Zdroj", "Preklad", "Jazyky", "Dátum")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=18)
        tree.heading("Zdroj", text="Pôvodný text")
        tree.heading("Preklad", text="Preklad")
        tree.heading("Jazyky", text="Jazyky")
        tree.heading("Dátum", text="Dátum")
        tree.column("Zdroj", width=240, anchor="w")
        tree.column("Preklad", width=240, anchor="w")
        tree.column("Jazyky", width=80, anchor="center")
        tree.column("Dátum", width=140, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", background=BG_CARD, foreground=TEXT_PRIMARY,
                        fieldbackground=BG_CARD, rowheight=28, font=("SF Pro Display", 11))
        style.configure("Treeview.Heading", background=BG_DARK, foreground=TEXT_SECONDARY,
                        font=("SF Pro Display", 11, "bold"))

        scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True, padx=(16, 0), pady=8)
        scrollbar.pack(side="left", fill="y", pady=8)

        self._record_ids = []

        def load_data(query=""):
            tree.delete(*tree.get_children())
            self._record_ids.clear()
            rows = self.db.search(query) if query else self.db.get_all()
            for row in rows:
                rid, src, tgt, sl, tl, dt = row
                self._record_ids.append(rid)
                tree.insert("", "end", values=(
                    src[:60] + ("..." if len(src) > 60 else ""),
                    tgt[:60] + ("..." if len(tgt) > 60 else ""),
                    f"{sl} → {tl}",
                    dt[:16]
                ))

        search_var.trace_add("write", lambda *_: load_data(search_var.get()))
        load_data()

        # Buttons
        btn_frame = tk.Frame(win, bg=BG_DARK, padx=16, pady=12)
        btn_frame.pack(fill="x")

        def copy_selected():
            sel = tree.selection()
            if sel:
                idx = tree.index(sel[0])
                rows = self.db.get_all()
                if idx < len(rows):
                    subprocess.run(["pbcopy"], input=rows[idx][2].encode())

        def delete_selected():
            sel = tree.selection()
            if sel:
                idx = tree.index(sel[0])
                if idx < len(self._record_ids):
                    self.db.delete(self._record_ids[idx])
                    load_data(search_var.get())

        tk.Button(btn_frame, text="Kopírovať preklad", bg=ACCENT, fg="white", relief="flat",
                  font=("SF Pro Display", 11), padx=12, pady=6, cursor="hand2",
                  command=copy_selected).pack(side="left", padx=(0, 8))

        tk.Button(btn_frame, text="Vymazať záznam", bg=ERROR, fg="white", relief="flat",
                  font=("SF Pro Display", 11), padx=12, pady=6, cursor="hand2",
                  command=delete_selected).pack(side="left")

        tk.Button(btn_frame, text="Zatvoriť", bg=BG_CARD, fg=TEXT_PRIMARY, relief="flat",
                  font=("SF Pro Display", 11), padx=12, pady=6, cursor="hand2",
                  command=win.destroy).pack(side="right")

        win.mainloop()
