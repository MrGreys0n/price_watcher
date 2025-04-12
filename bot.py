from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from fastapi import Depends
from sqlalchemy.orm import Session

from main import SessionLocal, User, get_db
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: Message):
    username = message.from_user.username
    chat_id = message.chat.id

    print(f"User {username} is trying to subscribe")

    db: Session = SessionLocal()
    user = db.query(User).filter_by(telegram_username=username).first()

    if user:
        if user.telegram_chat_id:
            await message.answer("❗ Вы уже подписаны на уведомления об изменении цен.")
            db.close()
            return
        user.telegram_chat_id = str(chat_id)
        db.commit()
        await message.answer("✅ Вы подписались на уведомления об изменении цен.")
    else:
        await message.answer("❗ Укажите ваш Telegram username в профиле сайта.")
    db.close()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
