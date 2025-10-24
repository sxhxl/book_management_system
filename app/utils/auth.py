import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings

def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
