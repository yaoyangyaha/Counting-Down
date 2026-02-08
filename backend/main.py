from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from db import engine
from fastapi.middleware.cors import CORSMiddleware
from auth import *
from models import User

app = FastAPI()

origins = [
    "https://.xtiantech.cn",
    "http://.xtiantech.cn",
    "http://",
    "https://",
    "http://:5173",
    "https://:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册
@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=username).first():
        raise HTTPException(400, "用户已存在")
    u = User(username=username, password_hash=hash_password(password))
    db.add(u)
    db.commit()
    return {"ok": True}


# 登录
@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    u = db.query(User).filter_by(username=username).first()
    if not u or not verify(password, u.password_hash):
        raise HTTPException(400, "账号或密码错误")
    return {"token": create_token(u.id)}


# 打卡（使用 MySQL NOW(3)）
@app.post("/checkin")
def checkin(user=Depends(get_current_user), db: Session = Depends(get_db)):
    today = date.today()
    try:
        db.execute(text("""
            INSERT INTO checkins (user_id, checkin_date, checkin_time)
            VALUES (:uid, CURDATE(), NOW(3))
        """), {"uid": user.id})
        db.commit()
    except:
        raise HTTPException(400, "今日已打卡")
    return {"ok": True}


# 排行榜
@app.get("/rank")
def rank(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT user_id, checkin_time
        FROM checkins
        WHERE checkin_date = CURDATE()
        ORDER BY checkin_time ASC, id ASC
        LIMIT 100
    """)).fetchall()

    return [
        {"rank": i + 1, "user_id": r[0], "time": str(r[1])}
        for i, r in enumerate(rows)
    ]
