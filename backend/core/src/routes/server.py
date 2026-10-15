from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_injector import attach_injector

from src.connections.pgsql.connection import PostgreSQLClient
from src.config.dependency_injection.container import container
from src.middleware.Tracing import TracingMiddleware
from src.routes.v1.router import router as v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = container.get(PostgreSQLClient)
    await client.connect()

    yield

    await client.disconnect()

app = FastAPI(
    title="Medical Field API",
    lifespan=lifespan,
    version="1.0.0",
    doc_url="/docs",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Operations related to user authentication and authorization",
        },
        {
            "name": "Attendance",
            "description": "Operations related to patient attendance records",
        },
        {
            "name": "Medical Record",
            "description": "Operations related to patient medical records",
        },
        {
            "name": "Professional",
            "description": "Operations related to healthcare professionals",
        }
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TracingMiddleware)

app.include_router(v1)
attach_injector(app, container)