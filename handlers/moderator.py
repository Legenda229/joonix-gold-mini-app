from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select

from database import SessionLocal, Order, User
from utils import get_compensation

router = Router()


async def is_mod(user_id: int) -> bool:
    async with SessionLocal() as session:
        user = await session.get(User, user_id)
        return user and user.is_moderator


@router.callback_query(F.data.startswith("process:"))
async def process_order(call: CallbackQuery):
    if not await is_mod(call.from_user.id):
        await call.answer("Нет прав", show_alert=True)
        return

    order_id = int(call.data.split(":")[1])

    async with SessionLocal() as session:
        order = await session.get(Order, order_id)

        if order.status != "pending":
            await call.answer("Уже обработано")
            return

        order.status = "completed"

        user = await session.get(User, order.user_id)
        user.gold_balance += order.gold_amount
        user.total_spent += order.price_rub

        await session.commit()

    await call.message.edit_caption(call.message.caption + "\n\n✅ Обработано")
    await call.answer("Готово")
