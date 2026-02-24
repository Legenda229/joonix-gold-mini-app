import json
from aiogram import Router, F, Bot
from aiogram.types import (
    Message, WebAppInfo, InlineKeyboardMarkup,
    InlineKeyboardButton
)
from sqlalchemy import select

from config import WEBAPP_URL, MOD_GROUP
from database import SessionLocal, User, Order
from utils import calc_price, calc_listing_price

router = Router()


async def get_or_create_user(tg_user):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.id == tg_user.id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                id=tg_user.id,
                username=tg_user.username,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
            )
            session.add(user)
            await session.commit()
        return user


@router.message(F.text == "/start")
async def start_cmd(message: Message):
    await get_or_create_user(message.from_user)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🚀 Открыть магазин",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]]
    )

    await message.answer(
        "✨ <b>Добро пожаловать в Joonix Gold!</b>\n"
        "Покупка Gold для Standoff 2 — быстро и безопасно.",
        reply_markup=kb
    )


# 🔥 WebApp → создание заказа
@router.message(F.web_app_data)
async def webapp_order(message: Message):
    data = json.loads(message.web_app_data.data)
    gold = int(data["gold"])

    price = calc_price(gold)
    listing = calc_listing_price(gold)

    async with SessionLocal() as session:
        user = await session.get(User, message.from_user.id)

        order = Order(
            user_id=user.id,
            gold_amount=gold,
            price_rub=price,
            listing_price=listing,
        )
        session.add(order)
        await session.commit()

    await message.answer(
        f"🧾 <b>Заказ создан</b>\n\n"
        f"💰 Gold: <b>{gold}</b>\n"
        f"💵 К оплате: <b>{price} RUB</b>\n\n"
        f"📸 Выставьте <b>M4 Flock</b> за <b>{listing} RUB</b>\n"
        f"и отправьте скриншот."
    )


@router.message(F.photo)
async def handle_screenshot(message: Message, bot: Bot):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Order)
            .where(Order.user_id == message.from_user.id)
            .where(Order.status == "pending")
            .order_by(Order.id.desc())
        )
        order = result.scalars().first()

        if not order:
            await message.answer("❌ Нет активного заказа.")
            return

        order.screenshot_file_id = message.photo[-1].file_id
        await session.commit()

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="✅ Process",
                callback_data=f"process:{order.id}"
            ),
            InlineKeyboardButton(
                text="❌ Reject",
                callback_data=f"reject:{order.id}"
            )
        ]]
    )

    await bot.send_photo(
        MOD_GROUP,
        photo=message.photo[-1].file_id,
        caption=(
            f"🆕 <b>Новый заказ</b>\n"
            f"👤 ID: <code>{message.from_user.id}</code>\n"
            f"💰 Gold: {order.gold_amount}\n"
            f"💵 Цена: {order.listing_price} RUB"
        ),
        reply_markup=kb
    )

    await message.answer("📩 Скриншот отправлен модератору.")
