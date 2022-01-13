from aiogram import executor
from aiogram.utils.executor import start_webhook

from data.config import WEBHOOK_URL, WEBHOOK_SSL_CERT, WEBHOOK_PATH, WEBHOOK_HOST, WEBHOOK_PORT
from loader import dp, ssl_context
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await dp.bot.set_webhook(
        url=WEBHOOK_URL,
        certificate=WEBHOOK_SSL_CERT
    )

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        host=WEBHOOK_HOST,
        port=WEBHOOK_PORT,
        ssl_context=ssl_context
    )

