import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


def init_database(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS forecast_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                model TEXT NOT NULL,
                horizon INTEGER NOT NULL,
                rows_in INTEGER NOT NULL,
                rows_clean INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


@contextmanager
def get_connection(path: Path) -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def record_run(
    path: Path,
    *,
    filename: str,
    model: str,
    horizon: int,
    rows_in: int,
    rows_clean: int,
) -> int:
    with get_connection(path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO forecast_runs
                (filename, model, horizon, rows_in, rows_clean, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                model,
                horizon,
                rows_in,
                rows_clean,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)
