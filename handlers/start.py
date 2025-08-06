# handlers/start.py

from aiogram import Router, types, F
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text.in_({"/start","🏠 Home"}))
async def cmd_start(msg: types.Message):
    await msg.answer(
        "👋 Welcome to AltPlace!\n\nFind, suggest, and explore great places to study/work/organise events.",
        reply_markup=main_menu
    )