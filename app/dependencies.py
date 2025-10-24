from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.auth import decode_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt_token(token)
        user_id: int = payload.get("sub")
        role: str = payload.get("role", "user")
        if user_id is None:
            raise HTTPException(status_code=401)
        return {"user_id": user_id, "role": role}
    except:
        raise HTTPException(status_code=401)

async def admin_only(user = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user
