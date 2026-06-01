import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.config/groq-translator/history.db")


class HistoryDB:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                source_lang TEXT,
                target_lang TEXT,
                created_at TEXT DEFAULT (datetime('now','localtime'))
            )
        """)
        self.conn.commit()

    def add(self, source: str, translated: str, src_lang: str, tgt_lang: str):
        self.conn.execute(
            "INSERT INTO history (source_text, translated_text, source_lang, target_lang) VALUES (?,?,?,?)",
            (source, translated, src_lang, tgt_lang),
        )
        self.conn.commit()

    def get_all(self, limit=200):
        cur = self.conn.execute(
            "SELECT id, source_text, translated_text, source_lang, target_lang, created_at FROM history ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return cur.fetchall()

    def search(self, query: str):
        q = f"%{query}%"
        cur = self.conn.execute(
            "SELECT id, source_text, translated_text, source_lang, target_lang, created_at FROM history WHERE source_text LIKE ? OR translated_text LIKE ? ORDER BY id DESC LIMIT 100",
            (q, q),
        )
        return cur.fetchall()

    def delete(self, record_id: int):
        self.conn.execute("DELETE FROM history WHERE id=?", (record_id,))
        self.conn.commit()

    def clear_all(self):
        self.conn.execute("DELETE FROM history")
        self.conn.commit()
