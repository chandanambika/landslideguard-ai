"""
SQLite Database Persistence Layer
Stores simulated alert events, inference history, and audit trails.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from backend.config import settings


def init_db():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Predictions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        region_name TEXT,
        risk_score REAL,
        risk_category TEXT,
        probability REAL,
        model_used TEXT,
        input_data TEXT,
        shap_summary TEXT
    )
    """)

    # Alerts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alert_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        risk_category TEXT,
        risk_score REAL,
        location TEXT,
        recipient_target TEXT,
        alert_message TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_prediction(data: Dict[str, Any], result: Dict[str, Any]):
    try:
        conn = sqlite3.connect(settings.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO prediction_logs (
            timestamp, latitude, longitude, region_name,
            risk_score, risk_category, probability,
            model_used, input_data, shap_summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            float(data.get("latitude", 0.0)),
            float(data.get("longitude", 0.0)),
            str(data.get("region_name", "Demo Sector")),
            float(result.get("risk_score", 0.0)),
            str(result.get("risk_category", "UNKNOWN")),
            float(result.get("probability", 0.0)),
            str(result.get("model_used", "XGBoost")),
            json.dumps(data),
            json.dumps(result.get("shap_explanation", {}).get("top_risk_factors", []))
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Warning: Database logging skipped ({e})")


def log_alert(alert_payload: Dict[str, Any]) -> int:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO alert_logs (
        timestamp, risk_category, risk_score,
        location, recipient_target, alert_message, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        alert_payload.get("risk_category", "LOW"),
        float(alert_payload.get("risk_score", 0.0)),
        alert_payload.get("location", "Unknown Location"),
        alert_payload.get("recipient_target", "Simulated Civil Defense Dispatch"),
        alert_payload.get("alert_message", ""),
        "DISPATCHED (SIMULATED)"
    ))
    alert_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return alert_id


def get_recent_alerts(limit: int = 10) -> List[Dict[str, Any]]:
    try:
        conn = sqlite3.connect(settings.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alert_logs ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


# Auto-initialize database on import
init_db()
