from fastapi import FastAPI
from sqlalchemy import text

from app.database.connection import engine

import app.models

from app.api.v1.tickets import router as ticket_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as user_router



app = FastAPI(
    title="Customer Support AI Agent"
)

app.include_router(auth_router)
app.include_router(user_router, prefix="/api/v1")
app.include_router(ticket_router, prefix="/api/v1")

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