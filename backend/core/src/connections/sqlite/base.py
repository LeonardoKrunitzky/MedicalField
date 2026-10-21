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