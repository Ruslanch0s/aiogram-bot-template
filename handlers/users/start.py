from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
import asyncpg.exceptions
import logging

# for postgresql
from utils.db_api.django_commands import add_user, select_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await add_user(user_id=message.from_user.id, full_name=message.from_user.full_name, username=message.from_user.username)
        name = message.from_user.full_name
    except Exception as err:
        logging.error(err)
        user = await select_user(user_id=message.from_user.id)
        name = user.name

    await message.answer(name)