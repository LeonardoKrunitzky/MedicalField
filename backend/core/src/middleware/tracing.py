import os
import time
import httpx
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError

from src.utils.jwt import decode_access_token
from src.connections.sqlite.connection import SQLiteClient


class TracingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to trace HTTP requests:
    - When is_offline=true: Saves to the offline_audit_logs table in SQLite.
    - When is_offline=false (Online): Sends asynchronously to the Go service.
    """

    def __init__(self, app):
        super().__init__(app)
        self.tracing_url = os.getenv("TRACING_URL", "http://localhost:8080/log")
        self.sqlite = SQLiteClient()

    async def dispatch(self, request: Request, call_next):
        """
        Process the request, validate authentication for specific routes, 
        and log the execution metrics.
        """
        path = request.url.path

        ignored_prefixes = (
            "/core/usecases/professional/login",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/favicon.ico",
        )
        if path.startswith(ignored_prefixes):
            return await call_next(request)

        professional_id = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = decode_access_token(token)
                professional_id = payload.get("sub")
            except JWTError:
                pass

        # Bloqueia o acesso caso a rota exija login e o token seja inválido/inexistente
        if path.startswith("/core/usecases/professional/") and not professional_id:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        is_offline_query = request.query_params.get("is_offline", "false").lower()
        is_offline_header = request.headers.get("X-Is-Offline", "false").lower()
        is_offline = is_offline_query in ("true", "1") or is_offline_header in ("true", "1")

        start_time = time.time()
        response = await call_next(request)
        processing_time_ms = int((time.time() - start_time) * 1000)

        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.headers.get(
                "X-Real-IP", request.client.host if request.client else "unknown"
            )

        log_data = {
            "client_ip": client_ip,
            "professional_id": str(professional_id) if professional_id else None,
            "http_method": request.method,
            "route": path,
            "status_code": response.status_code,
            "processing_time_ms": processing_time_ms,
        }

        if is_offline:
            await self._save_log_sqlite(log_data)
        else:
            asyncio.create_task(self._post_trace(log_data))

        return response

    async def _post_trace(self, log_data: dict) -> None:
        """
        Send the trace log to the Go microservice. 
        Fallback to offline SQLite storage on failure.
        """
        if not self.tracing_url:
            await self._save_log_sqlite(log_data)
            return

        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(self.tracing_url, json=log_data, timeout=3.0)
                res.raise_for_status()
            except Exception as e:
                print(f"Erro ao enviar log para Go [{type(e).__name__}]: salvando no SQLite.")
                await self._save_log_sqlite(log_data)

    async def _save_log_sqlite(self, log_data: dict) -> None:
        """
        Save the log in the offline_audit_logs SQLite table with is_synced = 0.
        """
        try:
            now = datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat()
            
            # Aguarda a conexão assíncrona antes de usar no context manager
            conn = await self.sqlite.get_connection()
            with conn:
                conn.execute(
                    """
                    INSERT INTO offline_audit_logs 
                    (client_ip, professional_id, http_method, route, status_code, processing_time_ms, created_at, is_synced)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                    """,
                    (
                        f"{log_data['client_ip']} (Offline SQLite)",
                        log_data["professional_id"],
                        log_data["http_method"],
                        log_data["route"],
                        log_data["status_code"],
                        log_data["processing_time_ms"],
                        now,
                    ),
                )
                conn.commit()
        except Exception as sqlite_err:
            print(f"Erro ao salvar log offline no SQLite: {sqlite_err}")