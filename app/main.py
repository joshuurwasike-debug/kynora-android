from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.contacts import router as contacts_router
from app.core.config import settings
from app.database.init_db import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Business Operations and Automation Platform",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://localhost",
        "http://localhost",
        "capacitor://localhost"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount(
    "/app",
    StaticFiles(
        directory=Path(__file__).resolve().parent.parent / "frontend",
        html=True
    ),
    name="frontend"
)
app.include_router(auth_router)
app.include_router(contacts_router)

@app.get("/")
def home():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "status": "operational"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
