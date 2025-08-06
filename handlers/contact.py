from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

router = Router()

@router.message(F.text.in_({"/contact", "📞 Contact"}))
async def contact_command(message: types.Message):
    print("✅ Contact handler triggered")
    await message.answer(
        "📬 *Contact Us*\n\n"
        "Have a suggestion, issue, or want to collaborate?\n"
        "You can reach out via:\n\n"
        "📨 Telegram: [@Wolfie_08](https://t.me/Wolfie_08)\n"
        "📧 Email: kdiyorbek133@gmail.com\n\n"
        "We're happy to hear from you! 💌",
        parse_mode="Markdown"
    )

