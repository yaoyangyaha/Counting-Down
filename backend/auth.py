from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db import SessionLocal
from models import User

SECRET_KEY = "<SECRET KEY>"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    password = password.strip()
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password.strip(), hashed)


def create_token(user_id: int) -> str:
    return jwt.encode({"uid": user_id}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
) -> User:
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(401, "未登录")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.get(User, payload["uid"])
        if not user:
            raise
        return user
    except JWTError:
        raise HTTPException(401, "登录失效")
