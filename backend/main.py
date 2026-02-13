from fastapi import FastAPI, Depends, HTTPException, Response, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import date, datetime
from sqlalchemy import text
from db import engine
from models import Base, User
from schemas import RegisterBody, LoginBody
from auth import (
    get_db, hash_password, verify_password,
    create_token, get_current_user
)
import asyncio
import httpx

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
TURNSTILE_SECRET = "<YOUR TUNSTILE_SECRET>"


def verify_turnstile(token: str, remote_ip: str):
    response = httpx.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            "secret": TURNSTILE_SECRET,
            "response": token,
            "remoteip": remote_ip
        },
        timeout=5.0
    )

    result = response.json()
    print(result)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail="人机验证失败")


# =========================
# 注册
# =========================
@app.post("/register")
def register(data: RegisterBody, request: Request, db: Session = Depends(get_db)):
    verify_turnstile(data.turnstile_token, request.client.host)
    if db.query(User).filter_by(username=data.username).first():
        raise HTTPException(400, "用户已存在")
    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        points=0
    )
    db.add(user)
    db.commit()
    return {"ok": True}


# =========================
# 登录
# =========================
@app.post("/login")
def login(data: LoginBody, request: Request, response: Response, db: Session = Depends(get_db)):
    verify_turnstile(data.turnstile_token, request.client.host)
    user = db.query(User).filter_by(username=data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(400, "账号或密码错误")

    token = create_token(user.id)
    response.set_cookie(
        "token", token,
        httponly=True,
        max_age=60 * 60 * 24 * 365,  # 1年
        samesite="lax"
    )
    return {"username": user.username}


@app.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"username": user.username}


# =========================
# 签到 + 积分逻辑
# =========================
POINTS_TABLE = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]


@app.post("/checkin")
def checkin(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today = date.today()
    try:
        # 插入打卡记录
        db.execute(
            text("""
                INSERT INTO checkins (user_id, checkin_date, checkin_time)
                VALUES (:uid, CURDATE(), NOW(3))
            """),
            {"uid": user.id}
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "今日已打卡")

    # 查询今天所有打卡按时间排序
    rows = db.execute(
        text("""
            SELECT user_id
            FROM checkins
            WHERE checkin_date = CURDATE()
            ORDER BY checkin_time ASC
        """)
    ).all()

    # 找到当前用户排名
    rank = next((i + 1 for i, r in enumerate(rows) if r[0] == user.id), len(rows))

    # 根据排名给积分
    points_added = POINTS_TABLE[rank - 1] if rank <= len(POINTS_TABLE) else 0
    if points_added > 0:
        user.points = (user.points or 0) + points_added
        db.add(user)
        db.commit()

    return {"rank": rank, "points_added": points_added}


# =========================
# 今日实时排行榜（不动）
# =========================
@app.websocket("/ws/rank")
async def ws_rank(ws: WebSocket):
    await ws.accept()
    db = Session(engine)
    try:
        while True:
            rows = db.execute(text("""
                SELECT u.username, c.checkin_time
                FROM checkins c
                JOIN users u ON u.id = c.user_id
                WHERE c.checkin_date = CURDATE()
                ORDER BY c.checkin_time ASC
            """)).all()

            await ws.send_json([
                {"username": r[0], "checkin_time": str(r[1])}
                for r in rows
            ])
            await asyncio.sleep(1)
    finally:
        db.close()


# =========================
# 年度积分排行榜
# =========================
@app.get("/points/rank")
def points_rank(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT username, points
        FROM users
        ORDER BY points DESC, id ASC
        LIMIT 50
    """)).all()

    return [{"username": r[0], "points": r[1]} for r in rows]


# =========================
# 退出
# =========================
@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("token")
    return {"ok": True}
