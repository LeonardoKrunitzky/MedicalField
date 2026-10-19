from datetime import datetime
from zoneinfo import ZoneInfo
import sqlite3

from src.connections.sqlite.connection import SQLiteClient


class SqliteBase:
    """
    Base para os repositórios que operam no banco embarcado SQLite (Modo Offline).
    """

    def __init__(self, db: SQLiteClient) -> None:
        self.sqlite = db

    def _now_sp(self) -> str:
        return datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat()

    def _log_offline_action(
        self, conn: sqlite3.Connection, professional_id: str, method: str, route: str
    ) -> None:
        conn.execute(
            """
            INSERT INTO offline_audit_logs 
            (client_ip, professional_id, http_method, route, status_code, processing_time_ms, created_at, is_synced)
            VALUES (?, ?, ?, ?, 201, 5, ?, 0)
            """,
            (
                "127.0.0.1 (Offline SQLite)",
                str(professional_id),
                method,
                route,
                self._now_sp(),
            ),
        )