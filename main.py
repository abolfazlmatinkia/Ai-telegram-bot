from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.client.session.aiohttp import AiohttpSession
import asyncio, os, openai, datetime
from utils.auth import check_user_limit, is_subscribed
from utils.textgen import generate_article
from utils.speech import text_to_speech
from utils.payments import check_payment_status

bot_token = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    user_id = str(message.from_user.id)
    if not await is_subscribed(user_id):
        await message.answer("⛔️ برای استفاده نامحدود از ربات اشتراک تهیه کنید.")
        return
    if not await check_user_limit(user_id):
        await message.answer("📌 حد پیام رایگان امروز تمام شده.")
        return

    prompt = message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message["content"]
    await message.answer(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
