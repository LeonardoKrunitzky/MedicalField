import sqlite3
from pathlib import Path
from typing import Optional

from src.connections.base import BaseClient

DB_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "mysqlite_db"
    / "medicalfield_offline.db"
)


class SQLiteClient(BaseClient):
    _instance: Optional["SQLiteClient"] = None
    _is_connected: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db()
            cls._instance._is_connected = True
            print(f"[SQLite] Banco local criado/carregado em: {DB_PATH}")
        return cls._instance

    async def connect(self) -> None:
        if self._is_connected and DB_PATH.exists():
            return

        try:
            self._init_db()
            self._is_connected = True
            print(f"Connected to SQLite at {DB_PATH}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SQLite: {e}")

    async def disconnect(self) -> None:
        if self._is_connected:
            self._is_connected = False
            print("Disconnected from SQLite")

    async def ensure_connected(self) -> bool:
        try:
            if not self._is_connected or not DB_PATH.exists():
                await self.connect()

            with self.get_connection() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception as e:
            print(f"SQLite connection check failed: {e}")
            raise ConnectionError(f"SQLite is not connected: {e}")

    def get_connection(self) -> sqlite3.Connection:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Catálogo local de Medicamentos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS medications (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    standard_dosage TEXT,
                    created_at TEXT
                );
            """)

            # 2. Profissionais
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS professionals (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    professional_registration TEXT NOT NULL,
                    password TEXT NOT NULL,
                    created_at TEXT
                );
            """)

            # 3. Pacientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    document TEXT NOT NULL,
                    created_at TEXT,
                    is_synced INTEGER DEFAULT 0
                );
            """)

            # 4. Prontuários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS medical_records (
                    id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    created_at TEXT,
                    blood_type TEXT,
                    known_allergies TEXT,
                    chronic_conditions TEXT,
                    emergency_contact TEXT,
                    is_synced INTEGER DEFAULT 0
                );
            """)

            # 5. Atendimentos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendances (
                    id TEXT PRIMARY KEY,
                    medical_record_id TEXT NOT NULL,
                    professional_id TEXT NOT NULL,
                    created_at TEXT,
                    pressure TEXT,
                    heart_rate INTEGER,
                    consciousness_level INTEGER,
                    triage_protocol TEXT,
                    notes TEXT,
                    patient_id TEXT,
                    medications_json TEXT,
                    is_synced INTEGER DEFAULT 0
                );
            """)

            # 7. Logs de Auditoria Offline
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS offline_audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT,
                    client_ip TEXT,
                    professional_id TEXT,
                    http_method TEXT,
                    route TEXT,
                    status_code INTEGER,
                    processing_time_ms INTEGER,
                    is_synced INTEGER DEFAULT 0
                );
            """)
            conn.commit()