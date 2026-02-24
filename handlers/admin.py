from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_ID

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(F.text.startswith("/broadcast"))
async def broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer("📢 Рассылка поставлена в очередь (заглушка).")
