# handlers/my_meetups.py

from aiogram import Router, types, F
from database.supabase_client import supabase
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text.in_({"/my_meetups", "📅 My_Meetups"}))
async def show_my_meetups(msg: types.Message, state: FSMContext):
    telegram_id = msg.from_user.id

    # Step 1: Fetch user
    user = supabase.table("users").select("id").eq("telegram_id", telegram_id).maybe_single().execute()

    if user is None or user.data is None:
        await msg.answer("❌ You need to be registered to view your meetups.")
        return

    user_id = user.data["id"]

    # Step 2: Fetch meetups by host
    meetups = supabase.table("meetups") \
        .select("*") \
        .eq("host", user_id) \
        .order("event_date", desc=False) \
        .execute()

    if not meetups.data:
        await msg.answer("📭 You haven’t created any meetups yet.")
        return

    await state.update_data(my_meetups=meetups.data, page=0)
    await show_my_meetup_card(msg, state)

async def show_my_meetup_card(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    meetups = data["my_meetups"]
    page = data.get("page", 0)

    m = meetups[page]

    text = (
        f"📌 <b>{m['title']}</b> in <b>{m['city']}</b>\n"
        f"🗓️ {m['event_date']} at {m['time'] or 'Unknown'}\n"
        f"📍 {m['location'] or 'TBD'}\n\n"
        f"{m['description'] or ''}\n\n"
        f"🧾 {page + 1} of {len(meetups)}"
    )

    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Prev", callback_data="my_meetup_prev"))
    if page < len(meetups) - 1:
        buttons.append(InlineKeyboardButton(text="Next ➡️", callback_data="my_meetup_next"))

    markup = InlineKeyboardMarkup(inline_keyboard=[buttons]) if buttons else None
    await msg.answer(text, parse_mode="HTML", reply_markup=markup)

@router.callback_query(F.data.in_({"my_meetup_next", "my_meetup_prev"}))
async def paginate_my_meetups(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 0)

    if call.data == "my_meetup_next":
        page += 1
    elif call.data == "my_meetup_prev":
        page -= 1

    await state.update_data(page=page)
    await call.message.delete()
    await show_my_meetup_card(call.message, state)
