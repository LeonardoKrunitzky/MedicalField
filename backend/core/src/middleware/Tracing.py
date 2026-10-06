import os
import time
import httpx
import asyncio
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TracingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.tracing_url = os.getenv("TRACING_URL")

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/core/usecases/professional/login"):
            return await call_next(request)

        start_time = time.time()

        response = await call_next(request)

        processing_time_ms = int((time.time() - start_time) * 1000)

        professional_id = getattr(request.state, "professional_id", 0)

        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.headers.get(
                "X-Real-IP", request.client.host if request.client else "unknown"
            )

        log_data = {
            "client_ip": client_ip,
            "professional_id": professional_id,
            "http_method": request.method,
            "route": request.url.path,
            "status_code": response.status_code,
            "processing_time_ms": processing_time_ms,
        }

        asyncio.create_task(self._post_trace(log_data))

        return response

    async def _post_trace(self, log_data: dict):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(f"{self.tracing_url}", json=log_data, timeout=5.0)
            except Exception as e:
                print(f"Erro ao enviar log para Go [{type(e).__name__}]: {repr(e)}")
