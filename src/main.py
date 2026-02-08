from fastapi import FastAPI, HTTPException, status
from src.books.router import book_router
from contextlib import asynccontextmanager
from src.auth.routers import auth_router

import asyncpg
from src.db.main import init_db

# Define the lifespan event handlers for startup and shutdown
# These handlers will print messages when the server starts and stops.
# asynccontextmanager is used to create an asynchronous context manager for the lifespan events.
# contextlib.asynccontextmanager allows us to define setup and teardown logic for the FastAPI application.
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Server started")
    await init_db()
    yield
    print("server stop")

version = "v1"

app = FastAPI(lifespan=lifespan)

app.include_router(book_router, prefix="/book", tags=["books"])  
app.include_router(auth_router, prefix="/auth", tags=["auth"]) 