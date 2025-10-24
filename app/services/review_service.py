from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.schemas.review import Review as DBReview
from app.models.review import ReviewCreate, Review
from .ai_service import generate_summary

async def create_review(db: AsyncSession, book_id: int, review: ReviewCreate) -> Review:
    db_review = DBReview(book_id=book_id, **review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return Review.from_orm(db_review)

async def get_reviews_for_book(db: AsyncSession, book_id: int) -> list[Review]:
    result = await db.execute(select(DBReview).where(DBReview.book_id == book_id))
    return [Review.from_orm(r) for r in result.scalars().all()]

async def get_book_summary_and_rating(db: AsyncSession, book_id: int) -> dict:
    reviews = await get_reviews_for_book(db, book_id)
    texts = [r.review_text for r in reviews]
    summary = await generate_summary(" ".join(texts)) if texts else ""
    avg = (await db.execute(select(func.avg(DBReview.rating)).where(DBReview.book_id == book_id))).scalar() or 0
    return {"summary": summary, "average_rating": round(avg, 2)}
