from aiogram import Router, types, F
from database.supabase_client import supabase

router = Router()

@router.message(F.text.in_({"/libraries", "🏛 Libraries"}))
async def list_libraries(msg: types.Message):
    try:
        response = supabase.table("places").select("*").eq("category", "library").execute()

        if not response.data:
            await msg.answer("📚 No libraries found at the moment.")
            return

        for lib in response.data:
            text = (
                f"📚 *{lib['name']}* in *{lib['city']}*\n"
                f"🧾 {lib['description']}\n"
                f"📍 {lib['location']}\n"
                f"🏷️ Tags: {', '.join(lib['tags']) if lib.get('tags') else 'None'}"
            )
            await msg.answer(text, parse_mode="Markdown")

    except Exception as e:
        await msg.answer("⚠️ Failed to load libraries. Please try again later.")
        print(f"[libraries.py] Error: {e}")
