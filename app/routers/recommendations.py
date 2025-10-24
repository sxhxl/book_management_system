from fastapi import APIRouter, Depends, Query
from app.schemas.base import get_db
from app.dependencies import get_current_user
from app.services.book_service import get_recommendations
from app.models.book import Book

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/", response_model=list[Book])
async def recs(genres: list[str] = Query(...), db = Depends(get_db), user = Depends(get_current_user)):
    result = await db.execute(select(DBBook).where(DBBook.genre.in_(genres)))
    return [Book.from_orm(b) for b in result.scalars().all()]
