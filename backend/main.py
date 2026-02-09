from fastapi import FastAPI, Depends, HTTPException, Response, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import text
from db import engine
from models import Base, User
from schemas import RegisterBody, LoginBody
from auth import (
    get_db, hash_password, verify_password,
    create_token, get_current_user
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
def register(data: RegisterBody, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=data.username).first():
        raise HTTPException(400, "用户已存在")
    user = User(
        username=data.username,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    return {"ok": True}


@app.post("/login")
def login(data: LoginBody, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(400, "账号或密码错误")

    token = create_token(user.id)
    response.set_cookie(
        "token", token,
        httponly=True,
        max_age=60 * 60 * 24 * 30,
        samesite="lax"
    )
    return {"username": user.username}


@app.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"username": user.username}


@app.post("/checkin")
def checkin(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    today = date.today()
    try:
        db.execute(
            text("""
              INSERT INTO checkins (user_id, checkin_date, checkin_time)
              VALUES (:uid, CURDATE(), NOW(3))
            """),
            {"uid": user.id}
        )
        db.commit()
    except:
        raise HTTPException(400, "今日已打卡")
    return {"ok": True}


@app.websocket("/ws/rank")
async def ws_rank(ws: WebSocket):
    await ws.accept()
    while True:
        rows = engine.execute(text("""
          SELECT u.username, c.checkin_time
          FROM checkins c
          JOIN users u ON u.id = c.user_id
          WHERE c.checkin_date = CURDATE()
          ORDER BY c.checkin_time ASC
        """)).fetchall()
        await ws.send_json([
            {"username": r[0], "time": str(r[1])} for r in rows
        ])
