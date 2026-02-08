from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db import SessionLocal
from models import User

SECRET_KEY = "<SECRET KEY>"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(uid: int):
    return jwt.encode({"uid": uid}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(401, "未登录")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.get(User, payload["uid"])
        if not user:
            raise
        return user
    except:
        raise HTTPException(401, "登录失效")
