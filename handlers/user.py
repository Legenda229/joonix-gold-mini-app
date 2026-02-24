from aiogram import Router, F, Bot
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select

from config import WEBAPP_URL, MOD_GROUP
from database import SessionLocal, User, Order

router = Router()


async def get_or_create_user(tg_user):
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.id == tg_user.id))
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
        "✨ <b>Добро пожаловать в Joonix Gold!</b>\n\n"
        "Здесь вы можете безопасно приобрести Gold для Standoff 2.",
        reply_markup=kb
    )


@router.message(F.photo)
async def handle_screenshot(message: Message, bot: Bot):
    async with SessionLocal() as session:
        user = await session.get(User, message.from_user.id)

        order = Order(
            user_id=user.id,
            gold_amount=0,
            price_rub=0,
            listing_price=0,
            screenshot_file_id=message.photo[-1].file_id,
        )
        session.add(order)
        await session.commit()

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Process", callback_data=f"process:{order.id}"),
                InlineKeyboardButton(text="❌ Reject", callback_data=f"reject:{order.id}")
            ]
        ]
    )

    await bot.send_photo(
        MOD_GROUP,
        photo=message.photo[-1].file_id,
        caption=(
            f"🆕 <b>Новый заказ</b>\n"
            f"👤 ID: <code>{message.from_user.id}</code>"
        ),
        reply_markup=kb
    )

    await message.answer(
        "📩 Скриншот получен!\n"
        "⏳ Заказ отправлен на проверку модератору."
    )
