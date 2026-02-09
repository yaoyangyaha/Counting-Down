# backend/auth.py
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db import SessionLocal
from models import User

# =====================
# JWT 配置
# =====================
SECRET_KEY = "CHANGE_ME_TO_RANDOM_STRING"
ALGORITHM = "HS256"

# =====================
# 密码加密器
# =====================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =====================
# DB 依赖
# =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================
# 密码相关函数（🔥 就是你缺的）
# =====================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)



def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# =====================
# JWT 相关
# =====================
def create_token(user_id: int) -> str:
    return jwt.encode({"uid": user_id}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
) -> User:
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="未登录")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.get(User, payload["uid"])
        if not user:
            raise
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="登录失效")
