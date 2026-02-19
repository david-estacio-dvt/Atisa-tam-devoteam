import sqlite3
import json
import os
from datetime import datetime

class DatabaseService:
    def __init__(self, db_path="hr_agent_data.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Prompts Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_prompts (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP
            )
        ''')

        # Reports History Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP,
                report_type TEXT,
                target_entity TEXT,
                report_content TEXT,
                raw_data_json TEXT
            )
        ''')
        
        # Competitors Status Table (Snapshots)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS competitor_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP,
                name TEXT,
                visibility_score REAL,
                sentiment TEXT,
                topic TEXT,
                products_json TEXT
            )
        ''')

        conn.commit()
        conn.close()

    # --- Prompts ---
    def get_prompt(self, key, default_value=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM system_prompts WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return row[0]
        elif default_value:
            # Save default if not exists
            self.save_prompt(key, default_value)
            return default_value
        return None

    def save_prompt(self, key, value):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO system_prompts (key, value, updated_at) 
            VALUES (?, ?, ?) 
            ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
        """, (key, value, datetime.now()))
        conn.commit()
        conn.close()

    # --- Reports ---
    def save_report(self, report_type, target_entity, content, raw_data=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        raw_json = json.dumps(raw_data, default=str) if raw_data else None
        
        cursor.execute("""
            INSERT INTO reports_history (timestamp, report_type, target_entity, report_content, raw_data_json)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now(), report_type, target_entity, content, raw_json))
        conn.commit()
        conn.close()

    def get_history(self, limit=20):
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports_history ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    # --- Competitor Snapshots ---
    def save_competitor_snapshot(self, name, visibility, sentiment, topic, products=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        products_json = json.dumps(products) if products else None
        
        cursor.execute("""
            INSERT INTO competitor_snapshots (timestamp, name, visibility_score, sentiment, topic, products_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (datetime.now(), name, visibility, sentiment, topic, products_json))
        conn.commit()
        conn.close()
