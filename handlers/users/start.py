from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
import asyncpg.exceptions


# for postgresql
from utils.db_api import example
from utils.db_api.schemas.user import User


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    id = message.from_user.id
    try:
        user = await User(
            name=message.from_user.username,
            id=id
        ).create()
    except asyncpg.UniqueViolationError:
        user = await User.get(id)

    await message.answer(f"Привет, {user.name}!")
