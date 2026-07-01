from fastapi import FastAPI
from sqlalchemy import text

from app.database.connection import engine
from app.database.base import Base

import app.models

from app.api.v1.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Customer Support AI Agent"
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Customer Support AI Agent"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1 AS status"))
        value = result.scalar()

    return {
        "database": "Connected",
        "result": value
    }