from pydantic import BaseModel, Field
from typing import Optional,List
from fastapi import FastAPI,HTTPException
app=FastAPI()
books_db=[]
next_id=1
class BookCreate(BaseModel):
    title:str=Field(min_length=1,max_length=100)
    author:str=Field(min_length=2)
    price:float=Field(gt=0)
    pages:int=Field(ge=1)
    isbn:Optional[str]=None

class BookResponse(BaseModel):
    id:int
    title:str
    author:str
    price:float
    pages:int
    isbn:Optional[str]=None
@app.post("/books",response_model=BookResponse)
def creat_book(book:BookCreate):
    global next_id
    new_book={
        "id":next_id,
        "title":book.title,
        "author":book.author,
        "price":book.price,
        "pages":book.pages,
        "isbn":book.isbn
    }
    books_db.append(new_book)
    next_id+=1
    return new_book

@app.get("/books",response_model=List[BookResponse])
def get_all_books():
    return books_db

@app.get("/books/{book_id}",response_model=BookResponse)
def get_book_by_id(book_id:int):
    for book in books_db:
        if book["id"]==book_id:
            return book
    raise HTTPException(status_code=404,detail=f"Book is {book_id} Not Found")
@app.put("/books/{book_id}",response_model=BookResponse)
def update_book_by_id(book_id:int,updated_book:BookCreate):
    for i,book in enumerate(books_db):
        if book["id"]==book_id:
            books_db[i]={
                "id": book_id,
                "title": updated_book.title,
                "author": updated_book.author,
                "price": updated_book.price,
                "pages": updated_book.pages,
                "isbn": updated_book.isbn
            }
            return books_db[i]
    raise HTTPException(status_code=404,detail=f"Book is {book_id} Not Found")

@app.delete("/books/{book_id}",response_model=BookResponse)
def delete_book(book_id:int):
    for i,book in enumerate(books_db):
        if book["id"]==book_id:
            deleted_book=books_db.pop(i)
            return {"message":f"The {deleted_book} is Deleted Successfully"}
    raise HTTPException(status_code=404,detail=f"Book is {book_id} Not Found")
