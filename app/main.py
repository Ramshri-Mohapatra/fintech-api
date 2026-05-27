from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, transactions

app = FastAPI(title = "Fintech API", description = "Personal finance tracker API with JWT authentication, built with FastAPI and PostgreSQL", version = "1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return{"message": "Fintech API is running", "docs": "/docs"}
    