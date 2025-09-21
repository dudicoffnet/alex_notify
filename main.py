from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
import asyncio
import os
import datetime

TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
ALLOWED_IDS = list(map(int, os.getenv("ALLOWED_IDS", str(OWNER_ID)).split(",")))

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)

def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_IDS

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("🤖 Бот запущен и готов к работе.")

@router.message(Command("ping"))
async def cmd_ping(message: Message):
    await message.answer("🏓 Pong!")

@router.message(Command("report"))
async def cmd_report(message: Message):
    if not is_authorized(message.from_user.id):
        await message.answer("⛔ У вас нет доступа к этой команде.")
        return
    report_content = f"📄 Отчет от {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    with open("payloads/daily_report.txt", "w", encoding="utf-8") as f:
        f.write(report_content)
    file = FSInputFile("payloads/daily_report.txt", filename="daily_report.txt")
    await message.answer_document(file, caption="🗂 Актуальный отчет")

@router.message(Command("sendzip"))
async def cmd_sendzip(message: Message):
    if not is_authorized(message.from_user.id):
        await message.answer("⛔ У вас нет доступа к архивам.")
        return
    zip_path = "payloads/project_payload.zip"
    if not os.path.exists(zip_path):
        await message.answer("⚠️ Архив не найден. Сначала сформируй его.")
        return
    file = FSInputFile(zip_path, filename="project_payload.zip")
    await message.answer_document(file, caption="📦 Последний собранный архив")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())