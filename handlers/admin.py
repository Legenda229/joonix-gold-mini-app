from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select

from config import ADMIN_ID
from database import SessionLocal, User

router = Router()


def is_admin(uid: int):
    return uid == ADMIN_ID


@router.message(F.text.startswith("/addmod"))
async def add_mod(message: Message):
    if not is_admin(message.from_user.id):
        return

    user_id = int(message.text.split()[1])

    async with SessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            user.is_moderator = True
            await session.commit()

    await message.answer("✅ Модератор добавлен")
