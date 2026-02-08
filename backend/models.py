from sqlalchemy import Column, BigInteger, String, Date, ForeignKey
from sqlalchemy.dialects.mysql import DATETIME
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)


class Checkin(Base):
    __tablename__ = "checkins"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    checkin_date = Column(Date, nullable=False)
    checkin_time = Column(DATETIME(fsp=3), nullable=False)
