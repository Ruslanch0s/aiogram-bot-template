from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
import asyncpg.exceptions


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            telegram_id=message.from_user.id
        )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    user = list(user)
    await message.answer(f"Привет, {user}!")
