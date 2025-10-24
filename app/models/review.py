from pydantic import BaseModel

class ReviewBase(BaseModel):
    review_text: str
    rating: float

class ReviewCreate(ReviewBase):
    user_id: int

class Review(ReviewBase):
    id: int
    book_id: int
    user_id: int

    class Config:
        from_attributes = True
