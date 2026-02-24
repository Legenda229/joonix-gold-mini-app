from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime,
    Boolean, ForeignKey, Text
)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from config import DATABASE_URL

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)

    gold_balance = Column(Integer, default=0)
    total_spent = Column(Float, default=0)
    rejection_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    gold_amount = Column(Integer)
    price_rub = Column(Float)
    listing_price = Column(Float)

    status = Column(String, default="pending")
    rejection_reason = Column(Text, nullable=True)

    screenshot_file_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")


class PromoCode(Base):
    __tablename__ = "promocodes"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    gold_amount = Column(Integer)
    max_activations = Column(Integer)
    activations = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)


class PromoUsage(Base):
    __tablename__ = "promo_usage"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    promo_code = Column(String)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
