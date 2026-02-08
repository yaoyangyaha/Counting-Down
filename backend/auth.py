from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db import SessionLocal
from models import User

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"

pwd = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(p): return pwd.hash(p)


def verify(p, h): return pwd.verify(p, h)


def create_token(uid: int):
    return jwt.encode({"uid": uid}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.get(User, payload["uid"])
        if not user:
            raise
        return user
    except:
        raise HTTPException(401, "无效 token")
