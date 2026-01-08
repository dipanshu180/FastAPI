from fastapi import FastAPI, HTTPException, status
from src.books.book import book_router

app = FastAPI()

app.include_router(book_router, prefix="/book", tags=["books"])