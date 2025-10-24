from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.base import get_db
from app.dependencies import get_current_user, admin_only
from app.services.book_service import create_book, get_books, get_book_by_id, update_book, delete_book
from app.services.review_service import create_review, get_reviews_for_book, get_book_summary_and_rating
from app.models.book import BookCreate, Book
from app.models.review import ReviewCreate, Review

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=Book)
async def add_book(book: BookCreate, content: str = Query(None), db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    return await create_book(db, book, content)

@router.get("/", response_model=list[Book])
async def list_books(db: AsyncSession = Depends(get_db)):
    return await get_books(db)

@router.get("/{id}", response_model=Book)
async def get_book(id: int, db: AsyncSession = Depends(get_db)):
    return await get_book_by_id(db, id)

@router.put("/{id}", response_model=Book)
async def update(id: int, book: BookCreate, db: AsyncSession = Depends(get_db), user = Depends(admin_only)):
    return await update_book(db, id, book, user["role"])

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db), user = Depends(admin_only)):
    return await delete_book(db, id, user["role"])

@router.post("/{id}/reviews", response_model=Review)
async def add_review(id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    review.user_id = user["user_id"]
    return await create_review(db, id, review)

@router.get("/{id}/reviews", response_model=list[Review])
async def list_reviews(id: int, db: AsyncSession = Depends(get_db)):
    return await get_reviews_for_book(db, id)

@router.get("/{id}/summary")
async def summary(id: int, db: AsyncSession = Depends(get_db)):
    return await get_book_summary_and_rating(db, id)

@router.post("/generate-summary")
async def gen(content: str):
    from app.services.ai_service import generate_summary
    return {"summary": await generate_summary(content)}
