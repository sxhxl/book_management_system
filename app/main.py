from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.routers import books, recommendations
from app.utils.auth import create_jwt_token

app = FastAPI(title="Book AI System", docs_url="/docs")

app.include_router(books.router)
app.include_router(recommendations.router)

@app.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    if form.username == "user" and form.password == "pass":
        return {"access_token": create_jwt_token({"sub": 1, "role": "user"}), "token_type": "bearer"}
    if form.username == "admin" and form.password == "admin":
        return {"access_token": create_jwt_token({"sub": 1, "role": "admin"}), "token_type": "bearer"}
    raise HTTPException(401)
