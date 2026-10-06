from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_injector import attach_injector

from backend.core.src.config.dependency_injection import container
from backend.core.src.middleware.Tracing import TracingMiddleware
from backend.core.src.routes.v1 import router

app = FastAPI(
    title="Medical Field API",
    version="1.0.0",
    doc_url="/docs",
    openapi_url="/openapi.json",
    openapi_tags=[
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

app.include_router(router)
attach_injector(app, container)