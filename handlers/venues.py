from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.supabase_client import supabase

router = Router()

@router.message(F.text.in_({"/venues", "🏢 Venues"}))
async def list_venues(msg: types.Message):
    try:
        response = supabase.table("places").select("*").eq("category", "venue").execute()

        if not response.data:
            await msg.answer("🏛️ No venues found at the moment.")
            return

        for venue in response.data:
            text = (
                f"🏛️ *{venue['name']}* in *{venue['city']}*\n"
                f"🧾 {venue['description']}\n"
                f"📍 {venue['location']}\n"
                f"🏷️ Tags: {', '.join(venue['tags']) if venue.get('tags') else 'None'}"
            )
            await msg.answer(text, parse_mode="Markdown")

    except Exception as e:
        await msg.answer("⚠️ Failed to load venues. Please try again later.")
        print(f"[venues.py] Error: {e}")
