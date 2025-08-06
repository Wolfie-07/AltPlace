# handlers/help.py

from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(F.text.in_({"/help", "❓ Help"}))
async def help_handler(message: Message):
    await message.answer(
        "📖 *Help Menu* – List of available commands:\n\n"
        "🚀 /start – Begin your journey with Cafetté\n"
        "📍 /cafes – Browse laptop-friendly cafés near you\n"
        "🎯 /filter – Find cafés with your preferred features\n"
        "💡 /suggest – Recommend a new café to be added\n"
        "👤 /profile – View and manage your profile *(coming soon)*\n"
        "🤝 /meetup – Join public café meetups *(coming soon)*\n"
        "📅 /createmeetup – Organize your own meetup *(coming soon)*\n"
        "📬 /contact – Reach out with questions or feedback\n"
        "ℹ️ /help – Show this help message again\n\n"
        "_Need help deciding where to work today? I’ve got your back! ☕_",
        parse_mode="Markdown"
    )

