import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from handlers import routers  # imports your router list
from database.supabase_client import supabase  # optional: for test_connection()

# ✅ Set up logging
logging.basicConfig(level=logging.INFO)

# ✅ Initialize Bot and Dispatcher
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# ✅ Register all routers
for r in routers:
    dp.include_router(r)

# ✅ Optional: Test Supabase connection
def test_supabase_connection():
    try:
        result = supabase.table("users").select("*").limit(1).execute()
        logging.info("✅ Supabase connection successful")
    except Exception as e:
        logging.error(f"❌ Supabase connection failed: {e}")

async def main():
    test_supabase_connection()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
