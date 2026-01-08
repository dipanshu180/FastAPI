from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, status
from typing import Optional , List
from pydantic import BaseModel

book_router = APIRouter()


book = [{
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "year_published": 1925,
    "genre": "Fiction"  },
    
    {
    "id": 2,
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "year_published": 1960,
    "genre": "Fiction"  },

    {
    "id": 3,
    "title": "1984",
    "author": "George Orwell",
    "year_published": 1948,
    "genre": "Fiction"  },

]

class Book(BaseModel):
    id: int
    title: str
    author: str
    year_published: int
    genre: str

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str

@book_router.get("/",status_code=status.HTTP_200_OK)
async def get_all_books(response_model=list[Book]):
    return book 

@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def creat_book(new_book : Book ):
    new_book = new_book.model_dump()
    book.append(new_book)
    return new_book

@book_router.get("/{book_id}")
async def get_one_book(book_id : int):
    for b in book:
        if b["id"]==book_id:
            return b
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Book not found")

@book_router.patch("/{book_id}")
async def update_book(book_id : int , new_book: BookCreate):
    for b in book :
        if b["id"]==book_id:
            b["title"] = new_book.title
            b["author"] = new_book.author   
            b["genre"] = new_book.genre
            return b
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Book not found") 


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id : int):
    for b in book:
        if b["id"]==book_id:
            book.remove(b)
            return
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Book not found")