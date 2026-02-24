from aiogram import Router, F
from aiogram.types import CallbackQuery

from database import SessionLocal, Order, User
from utils import get_compensation

router = Router()


@router.callback_query(F.data.startswith("process:"))
async def process_order(call: CallbackQuery):
    order_id = int(call.data.split(":")[1])

    async with SessionLocal() as session:
        order = await session.get(Order, order_id)
        order.status = "completed"

        user = await session.get(User, order.user_id)
        user.gold_balance += order.gold_amount

        await session.commit()

    await call.message.edit_caption(call.message.caption + "\n\n✅ Обработано")
    await call.answer("Заказ выполнен")


@router.callback_query(F.data.startswith("reject:"))
async def reject_order(call: CallbackQuery):
    order_id = int(call.data.split(":")[1])

    async with SessionLocal() as session:
        order = await session.get(Order, order_id)
        order.status = "rejected"

        user = await session.get(User, order.user_id)
        user.rejection_count += 1

        if user.rejection_count >= 3:
            bonus = get_compensation(order.gold_amount)
            user.gold_balance += bonus
            user.rejection_count = 0

        await session.commit()

    await call.message.edit_caption(call.message.caption + "\n\n❌ Отклонено")
    await call.answer("Заказ отклонён")
