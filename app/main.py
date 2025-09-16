from fastapi import FastAPI
from .routes import accounts, transactions
from .database import Base, engine

app = FastAPI(title="Banking App")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(accounts.router)
app.include_router(transactions.router)
