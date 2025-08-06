from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.createmeetup import CreateMeetup
from database.supabase_client import supabase
from datetime import datetime

router = Router()

@router.message(F.text.in_({"/createmeetup", "➕ Create Meetup"}))
async def start_meetup(msg: types.Message, state: FSMContext):
    await msg.answer("📌 What's the title of the meetup?")
    await state.set_state(CreateMeetup.title)

@router.message(CreateMeetup.title)
async def get_title(msg: types.Message, state: FSMContext):
    await state.update_data(title=msg.text)
    await msg.answer("📝 Give a short description:")
    await state.set_state(CreateMeetup.description)

@router.message(CreateMeetup.description)
async def get_description(msg: types.Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.answer("📍 What's the location?")
    await state.set_state(CreateMeetup.location)

@router.message(CreateMeetup.location)
async def get_location(msg: types.Message, state: FSMContext):
    await state.update_data(location=msg.text)
    await msg.answer("🏙️ Which city is it in?")
    await state.set_state(CreateMeetup.city)

@router.message(CreateMeetup.city)
async def get_city(msg: types.Message, state: FSMContext):
    await state.update_data(city=msg.text)
    await msg.answer("🗓️ What's the date? (YYYY-MM-DD)")
    await state.set_state(CreateMeetup.event_date)

@router.message(CreateMeetup.event_date)
async def get_event_date(msg: types.Message, state: FSMContext):
    try:
        datetime.strptime(msg.text, "%Y-%m-%d")
    except ValueError:
        await msg.answer("⚠️ Please enter the date in YYYY-MM-DD format.")
        return

    await state.update_data(event_date=msg.text)
    await msg.answer("⏰ What time? (HH:MM, 24h format)")
    await state.set_state(CreateMeetup.time)

@router.message(CreateMeetup.time)
async def get_time(msg: types.Message, state: FSMContext):
    try:
        datetime.strptime(msg.text, "%H:%M")
    except ValueError:
        await msg.answer("⚠️ Please use the 24h time format: HH:MM")
        return

    await state.update_data(time=msg.text)

    data = await state.get_data()
    preview = (
        f"🆕 Meetup Preview:\n\n"
        f"📌 <b>{data['title']}</b>\n"
        f"📝 {data['description']}\n"
        f"📍 {data['location']} in {data['city']}\n"
        f"🗓️ {data['event_date']} at {data['time']}\n\n"
        f"✅ Type 'yes' to confirm or 'no' to cancel."
    )
    await msg.answer(preview, parse_mode="HTML")
    await state.set_state(CreateMeetup.confirm)

@router.message(CreateMeetup.confirm)
async def confirm_meetup(msg: types.Message, state: FSMContext):
    if msg.text.lower() != "yes":
        await msg.answer("❌ Meetup creation cancelled.")
        await state.clear()
        return

    data = await state.get_data()
    telegram_id = msg.from_user.id

    # Get or create user
    user = supabase.table("users").select("id").eq("telegram_id", telegram_id).maybe_single().execute()
    if not user.data:
        supabase.table("users").insert({
            "telegram_id": telegram_id,
            "username": msg.from_user.username or ""
        }).execute()
        user = supabase.table("users").select("id").eq("telegram_id", telegram_id).maybe_single().execute()

    if not user or not user.data:
        await msg.answer("⚠️ Couldn't verify your user. Please try again later.")
        await state.clear()
        return

    host_id = user.data["id"]

    # Insert the meetup
    supabase.table("meetups").insert({
        "title": data["title"],
        "description": data["description"],
        "location": data["location"],
        "city": data["city"],
        "event_date": data["event_date"],
        "time": data["time"],
        "host": host_id
    }).execute()

    await msg.answer("✅ Your meetup has been created!")
    await state.clear()
