import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("✅ Бот запущен и готов к работе.")

@router.message(Command("ping"))
async def ping_handler(message: Message):
    await message.answer("🏓 Pong!")


import requests

@router.message(Command("report"))


async def report_handler(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("⛔ Нет доступа")
        return

    try:
        response = requests.post("https://valik.ai/api/report", json={
            "questions": [
                "Варианты перелёта из Минска на Фукуок с 5 по 25 ноября (на двоих, 1 пересадка, до 24 ч)",
                "Снос/застройка улицы Мирной (район: Долгиновский, Старовиленский, Червякова, Пригородная)"
            ],
            "lang": "ru",
            "auth_token": "test_token_123"
        }, timeout=30)

        data = response.json()
        report = ""
        for q, a in data["answers"].items():
            report += f"❓ <b>{q}</b>\n💬 {a}\n\n"

        await message.answer(report[:4096])

    except Exception as e:
        await message.answer(f"⚠️ Ошибка при формировании отчёта: {str(e)}")

    if message.from_user.id != OWNER_ID:
        await message.answer("⛔ Нет доступа")
        return
    with open("payloads/daily_report.txt", "w", encoding="utf-8") as f:
        f.write("📄 Актуальный отчёт сформирован.")
    file = FSInputFile("payloads/daily_report.txt")
    await message.answer_document(file, caption="📄 Твой отчёт")

@router.message(Command("sendzip"))
async def sendzip_handler(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("⛔ Нет доступа")
        return
    zip_path = "payloads/project_payload.zip"
    if not os.path.exists(zip_path):
        await message.answer("⚠️ Архив не найден.")
        return
    file = FSInputFile(zip_path)
    await message.answer_document(file, caption="📦 Последний архив проекта")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())