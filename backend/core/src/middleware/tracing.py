import os
import time
import httpx
import asyncio
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError

from src.utils.jwt import decode_access_token


class TracingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to trace HTTP requests and asynchronously send log data to a Go microservice.
    """

    def __init__(self, app):
        """
        Initializes the tracing middleware with the application and tracing URL.
        """
        super().__init__(app)
        self.tracing_url = os.getenv("TRACING_URL")

    async def dispatch(self, request: Request, call_next):
        """
        Intercepts incoming requests, processes them, and logs metrics.
        """
        if request.url.path.startswith("/core/usecases/professional/"):
            return await call_next(request)

        start_time = time.time()
        response = await call_next(request)
        processing_time_ms = int((time.time() - start_time) * 1000)

        professional_id = 0
        auth_header = request.headers.get("Authorization")
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = decode_access_token(token)
                professional_id = payload.get("sub", 0)
            except JWTError:
                pass

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
        """
        Sends the collected log data payload asynchronously to the tracing service.
        """
        async with httpx.AsyncClient() as client:
            try:
                await client.post(f"{self.tracing_url}", json=log_data, timeout=5.0)
            except Exception as e:
                print(f"Erro ao enviar log para Go [{type(e).__name__}]: {repr(e)}")