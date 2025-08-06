# handlers/suggest.py
import os
from aiogram.types import Message
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.suggest import SuggestPlace
from database.supabase_client import supabase
from config import ADMIN_CHAT_ID
router = Router()


@router.message(F.text.in_({"/suggest", "📝 Suggest"}))
async def suggest_start(msg: types.Message, state: FSMContext):
    await msg.answer("What type of place are you suggesting? (cafe, library, venue, activity)")
    await state.set_state(SuggestPlace.category)

@router.message(SuggestPlace.category)
async def receive_category(msg: types.Message, state: FSMContext):
    await state.update_data(category=msg.text.lower())
    await msg.answer("Great! What's the name of the place?")
    await state.set_state(SuggestPlace.name)

@router.message(SuggestPlace.name)
async def receive_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Now send a short description.")
    await state.set_state(SuggestPlace.description)

@router.message(SuggestPlace.description)
async def receive_desc(msg: types.Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.answer("Which city is it in?")
    await state.set_state(SuggestPlace.city)

@router.message(SuggestPlace.city)
async def receive_city(msg: types.Message, state: FSMContext):
    await state.update_data(city=msg.text)
    await msg.answer("What's the address or location?")
    await state.set_state(SuggestPlace.location)

@router.message(SuggestPlace.location)
async def receive_location(msg: types.Message, state: FSMContext):
    await state.update_data(location=msg.text)
    await msg.answer("Finally, add tags separated by commas (e.g. wifi, quiet, power).")
    await state.set_state(SuggestPlace.tags)

@router.message(SuggestPlace.tags)
async def receive_tags(msg: types.Message, state: FSMContext):
    tags = [t.strip() for t in msg.text.split(",")]
    await state.update_data(tags=tags)
    data = await state.get_data()
    await msg.answer(
        f"Confirm submission?\n\n"
        f"📌 *{data['name']}* in *{data['city']}*\n"
        f"🧾 {data['description']}\n"
        f"📍 {data['location']}\n"
        f"🏷️ Tags: {', '.join(tags)}\n"
        f"📂 Category: {data['category']}\n\n"
        f"Type 'yes' to confirm or 'no' to cancel.",
        parse_mode="Markdown"
    )
    await state.set_state(SuggestPlace.confirm)

@router.message(SuggestPlace.confirm)
async def confirm_submission(msg: types.Message, state: FSMContext):
    if msg.text.lower() != "yes":
        await msg.answer("❌ Suggestion cancelled.")
        await state.clear()
        return

    data = await state.get_data()
    telegram_id = msg.from_user.id

    # 🚨 Replace this with the actual column name in Supabase if different
    TELEGRAM_ID_COL = "telegram_id"

    # Step 1: Try to fetch user
    user = supabase.table("users") \
        .select("id") \
        .eq(TELEGRAM_ID_COL, telegram_id) \
        .maybe_single() \
        .execute()

    # Step 2: If not found, insert and re-fetch
    if user is None or user.data is None:
        supabase.table("users").insert({
            TELEGRAM_ID_COL: telegram_id,
            "username": msg.from_user.username or ""
        }).execute()

        user = supabase.table("users") \
            .select("id") \
            .eq(TELEGRAM_ID_COL, telegram_id) \
            .maybe_single() \
            .execute()

    # Step 3: If still missing, abort
    if user is None or user.data is None:
        await msg.answer("⚠️ Failed to verify your user. Please try again later.")
        await state.clear()
        return

    user_id = user.data["id"]

    # Step 4: Insert place suggestion
    supabase.table("places").insert({
        "name": data["name"],
        "description": data["description"],
        "location": data["location"],
        "city": data["city"],
        "tags": data["tags"],
        "category": data["category"],
        "submitted_by": user_id
    }).execute()
    await msg.answer("✅ Your suggestion has been submitted! Thank you!")
    await state.clear()
    # Notify admin
    admin_msg = (
        f"New place suggestion:\n\n"
        f"📌 *{data['name']}* in *{data['city']}*\n"
        f"🧾 {data['description']}\n"
        f"📍 {data['location']}\n"
        f"🏷️ Tags: {', '.join(data['tags'])}\n"
        f"📂 Category: {data['category']}\n"
        f"👤 Suggested by: @{msg.from_user.username} (ID: {msg.from_user.id})"
    )
    await msg.bot.send_message(ADMIN_CHAT_ID, admin_msg, parse_mode="Markdown") 
    
