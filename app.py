import logging

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.db_api import db_gino, example
from utils.db_api.schemas.user import User
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # for postgresql
    print("Создаем подключение к БД")
    await db_gino.on_startup(dp)
    print("Очистить базу")
    await db.gino.drop_all()
    print("Создаем таблицу пользователей")
    await db.gino.create_all()
    print(await db.all(User.query))

    # Устанавливаем дефолтные команды "\start"
    await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
