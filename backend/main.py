from fastapi import FastAPI
from sqlalchemy.connectors import asyncio
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from auth import *
from db import SessionLocal
from ws_manager import ws_manager
from fastapi import HTTPException, Depends, Response
from sqlalchemy.orm import Session
from auth import verify_password, create_token, get_db
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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
def login(username: str, password: str, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(400, "账号或密码错误")

    if not verify_password(password, user.password_hash):
        raise HTTPException(400, "账号或密码错误")

    token = create_token(user.id)
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24 * 30,  # 30 天
        samesite="lax"
    )

    return {"username": user.username}


# 打卡（使用 MySQL NOW(3)）
@app.post("/checkin")
def checkin(user=Depends(get_current_user), db: Session = Depends(get_db)):
    # 插入今日打卡
    try:
        db.execute(text("""
            INSERT INTO checkins (user_id, checkin_date, checkin_time)
            VALUES (:uid, CURDATE(), NOW(3))
        """), {"uid": user.id})
        db.commit()
    except:
        raise HTTPException(400, "今日已打卡")

    # 查询最新排行榜
    rows = db.execute(text("""
        SELECT u.username, c.checkin_time
        FROM checkins c
        JOIN users u ON u.id = c.user_id
        WHERE c.checkin_date = CURDATE()
        ORDER BY c.checkin_time ASC
    """)).fetchall()

    data = [
        {"rank": i + 1, "username": r[0], "time": str(r[1])}
        for i, r in enumerate(rows)
    ]

    # 异步广播
    asyncio.create_task(ws_manager.broadcast(data))

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


@app.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username
    }
