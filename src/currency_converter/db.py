"""SQLite persistence: rate cache (TTL-based) and conversion history."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path.home() / ".currency_converter" / "data.db"
CACHE_TTL_MINUTES = 60

SCHEMA = """
CREATE TABLE IF NOT EXISTS rate_cache (
    base_currency TEXT NOT NULL,
    target_currency TEXT NOT NULL,
    rate REAL NOT NULL,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (base_currency, target_currency)
);

CREATE TABLE IF NOT EXISTS conversion_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    amount REAL NOT NULL,
    from_currency TEXT NOT NULL,
    to_currency TEXT NOT NULL,
    rate REAL NOT NULL,
    result REAL NOT NULL
);
"""


def get_connection() -> sqlite3.Connection:
    """Open the DB connection, creating the data dir/schema on first run."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    return conn


def get_cached_rate(conn: sqlite3.Connection, base: str, target: str) -> float | None:
    """Return a cached rate if present and younger than CACHE_TTL_MINUTES, else None."""
    row = conn.execute(
        "SELECT rate, fetched_at FROM rate_cache WHERE base_currency = ? AND target_currency = ?",
        (base.upper(), target.upper()),
    ).fetchone()
    if row is None:
        return None

    rate, fetched_at = row
    fetched_dt = datetime.fromisoformat(fetched_at)
    if datetime.now() - fetched_dt > timedelta(minutes=CACHE_TTL_MINUTES):
        return None
    return rate


def cache_rate(conn: sqlite3.Connection, base: str, target: str, rate: float) -> None:
    """Insert or refresh a cached rate for a currency pair."""
    conn.execute(
        "INSERT OR REPLACE INTO rate_cache (base_currency, target_currency, rate, fetched_at) "
        "VALUES (?, ?, ?, ?)",
        (base.upper(), target.upper(), rate, datetime.now().isoformat()),
    )
    conn.commit()


def log_conversion(
    conn: sqlite3.Connection, amount: float, base: str, target: str, rate: float, result: float
) -> None:
    """Append a completed conversion to history."""
    conn.execute(
        "INSERT INTO conversion_history (timestamp, amount, from_currency, to_currency, rate, result) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), amount, base.upper(), target.upper(), rate, result),
    )
    conn.commit()


def get_history(
    conn: sqlite3.Connection, limit: int = 10
) -> list[tuple[str, float, str, str, float, float]]:
    """Return the most recent conversions, newest first."""
    return conn.execute(
        "SELECT timestamp, amount, from_currency, to_currency, rate, result "
        "FROM conversion_history ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
