from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException
from app.schemas.book import Book as DBBook
from app.models.book import BookCreate, Book
from .ai_service import generate_summary

async def create_book(db: AsyncSession, book: BookCreate, content: str | None) -> Book:
    summary = await generate_summary(content) if content else None
    db_book = DBBook(**book.dict(), summary=summary)
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return Book.from_orm(db_book)

async def get_books(db: AsyncSession) -> list[Book]:
    result = await db.execute(select(DBBook))
    return [Book.from_orm(b) for b in result.scalars().all()]

async def get_book_by_id(db: AsyncSession, book_id: int) -> Book:
    result = await db.execute(select(DBBook).where(DBBook.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(404, "Book not found")
    return Book.from_orm(book)

async def update_book(db: AsyncSession, book_id: int, book_update: BookCreate, role: str) -> Book:
    if role != "admin":
        raise HTTPException(403)
    result = await db.execute(select(DBBook).where(DBBook.id == book_id))
    db_book = result.scalars().first()
    if not db_book:
        raise HTTPException(404)
    for k, v in book_update.dict(exclude_unset=True).items():
        setattr(db_book, k, v)
    await db.commit()
    await db.refresh(db_book)
    return Book.from_orm(db_book)

async def delete_book(db: AsyncSession, book_id: int, role: str):
    if role != "admin":
        raise HTTPException(403)
    result = await db.execute(select(DBBook).where(DBBook.id == book_id))
    db_book = result.scalars().first()
    if not db_book:
        raise HTTPException(404)
    await db.delete(db_book)
    await db.commit()
    return {"detail": "Deleted"}


async def get_recommendations(db: AsyncSession, genres: List[str]) -> List[Book]:
    """Recommend books by genre"""
    result = await db.execute(
        select(Book).where(Book.genre.in_(genres))
    )
    return result.scalars().all()
