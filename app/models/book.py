from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    summary: str | None = None

    class Config:
        from_attributes = True
