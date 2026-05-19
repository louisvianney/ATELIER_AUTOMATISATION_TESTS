import sqlite3
import json
from datetime import datetime

DB_PATH = "/home/UlrichVianney/runs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            api TEXT,
            passed INTEGER,
            failed INTEGER,
            error_rate REAL,
            latency_avg INTEGER,
            latency_p95 INTEGER,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_run(result):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO runs (timestamp, api, passed, failed, error_rate, latency_avg, latency_p95, details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        result["api"],
        result["summary"]["passed"],
        result["summary"]["failed"],
        result["summary"]["error_rate"],
        result["summary"]["latency_ms_avg"],
        result["summary"]["latency_ms_p95"],
        json.dumps(result["tests"])
    ))
    conn.commit()
    conn.close()

def list_runs(limit=20):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT id, timestamp, api, passed, failed, error_rate, latency_avg, latency_p95, details
        FROM runs ORDER BY id DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [{"id": r[0], "timestamp": r[1], "api": r[2], "passed": r[3],
             "failed": r[4], "error_rate": r[5], "latency_avg": r[6],
             "latency_p95": r[7], "tests": json.loads(r[8])} for r in rows]