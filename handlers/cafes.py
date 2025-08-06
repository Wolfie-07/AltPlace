from aiogram import Router, types, F
from aiogram.filters import Command
from database.supabase_client import supabase

router = Router()

@router.message(F.text.in_({"/cafes", "☕️ Cafes"}))
async def show_cafes(message: types.Message):
    # Get cafes from Supabase
    response = supabase.table("places").select("*").eq("category", "cafe").limit(10).execute()

    cafes = response.data
    if not cafes:
        await message.answer("☕ No cafés added yet. You can suggest one using /suggest!")
        return

    for cafe in cafes:
        tags = ", ".join(cafe.get("tags", [])) if isinstance(cafe.get("tags"), list) else cafe.get("tags", "")
        text = (
            f"🏠 <b>{cafe['name']}</b>\n"
            f"📍 <i>{cafe['location']}</i>\n"
            f"📖 {cafe.get('description', 'No description')}\n"
            f"🏷️ Tags: {tags}"
        )
        await message.answer(text, parse_mode="HTML")
