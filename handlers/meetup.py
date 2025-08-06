from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.supabase_client import supabase
from datetime import datetime

router = Router()

@router.message(F.text.in_({"/meetup", "📅 Meetups"}))
async def list_meetups(msg: types.Message, state: FSMContext):
    today = datetime.now().date().isoformat()

    # Fetch upcoming meetups ordered by date
    response = supabase.table("meetups").select("*") \
        .gte("event_date", today) \
        .order("event_date", desc=False) \
        .limit(10) \
        .execute()

    meetups = response.data

    if not meetups:
        await msg.answer("📭 No upcoming meetups yet. Check back soon or suggest one with /createmeetup!")
        return

    # Save to FSM for pagination
    await state.update_data(meetups=meetups, page=0)
    await show_meetup(msg, state)

async def show_meetup(msg_or_call: types.Message | types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    meetups = data["meetups"]
    page = data.get("page", 0)

    meetup = meetups[page]

    text = (
        f"📅 <b>{meetup['title']}</b>\n\n"
        f"📝 {meetup['description'] or 'No description'}\n"
        f"📍 {meetup['location'] or 'TBD'} in {meetup['city'] or 'Unknown'}\n"
        f"🗓️ {meetup['event_date']} at {meetup['time'] or 'TBD'}\n"
        f"🔗 Hosted by user ID: <code>{meetup['host'] or 'Unknown'}</code>\n"
        f"📄 {page + 1} of {len(meetups)}"
    )

    # Pagination buttons
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Prev", callback_data="meetup_prev"))
    if page < len(meetups) - 1:
        buttons.append(InlineKeyboardButton(text="Next ➡️", callback_data="meetup_next"))

    markup = InlineKeyboardMarkup(inline_keyboard=[buttons]) if buttons else None

    if isinstance(msg_or_call, types.Message):
        await msg_or_call.answer(text, parse_mode="HTML", reply_markup=markup)
    else:
        await msg_or_call.message.edit_text(text, parse_mode="HTML", reply_markup=markup)
        await msg_or_call.answer()

@router.callback_query(F.data.in_({"meetup_prev", "meetup_next"}))
async def paginate_meetups(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 0)

    if call.data == "meetup_next":
        page += 1
    elif call.data == "meetup_prev":
        page -= 1

    await state.update_data(page=page)
    await show_meetup(call, state)
