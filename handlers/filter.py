# handlers/filter.py
import os
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from states.filter import FilterPlace
from database.supabase_client import supabase

router = Router()

# Step 1: Start filtering
@router.message(F.text.in_({"/filter", "🔍 Filter"}))
async def start_filtering(msg: types.Message, state: FSMContext):
    cities = [
        "Tashkent", "Nurafshon", "Samarkand", "Bukhara", "Khiva",
        "Urganch", "Margilan", "Andijan", "Fergana", "Namangan",
        "Nukus", "Navoi", "Kokand", "Guliston", "Shakhrisabz"
    ]
    # Chunk cities into rows of 3
    city_buttons = [
        [InlineKeyboardButton(text=city, callback_data=f"city:{city}") for city in cities[i:i+3]]
        for i in range(0, len(cities), 3)
    ]
    # Add Cancel button as the last row
    city_buttons.append([
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")
    ])
    keyboard = InlineKeyboardMarkup(inline_keyboard=city_buttons)

    await msg.answer("📍 Choose a city:", reply_markup=keyboard)
    await state.set_state(FilterPlace.city)

# Step 2: Handle city selection from inline buttons
@router.callback_query(F.data.startswith("city:"))
async def handle_city_choice(call: CallbackQuery, state: FSMContext):
    city = call.data.split(":")[1]
    await state.update_data(city=city)
    await call.message.edit_text(f"✅ City selected: *{city}*\n\n📂 What category? (e.g. cafe, library, etc.)", parse_mode="Markdown")
    await state.set_state(FilterPlace.category)

# Step 3: Get category
@router.message(FilterPlace.category)
async def get_category(msg: types.Message, state: FSMContext):
    await state.update_data(category=msg.text.lower())
    await msg.answer("🏷️ Enter tags separated by commas (or leave blank to skip):")
    await state.set_state(FilterPlace.tags)

# Step 4: Get tags and show results
@router.message(FilterPlace.tags)
async def get_tags(msg: types.Message, state: FSMContext):
    tags = [t.strip().lower() for t in msg.text.split(",") if t.strip()]
    await state.update_data(tags=tags)

    data = await state.get_data()
    city = data["city"]
    category = data["category"]

    # Supabase query
    query = supabase.table("places").select("*") \
        .eq("city", city).eq("category", category)

    if tags:
        response = query.execute()
        filtered = [place for place in response.data if any(tag in place.get("tags", []) for tag in tags)]
    else:
        filtered = query.execute().data

    if not filtered:
        await msg.answer("❌ No places found. Try again with different filters.")
        await state.clear()
        return

    await state.update_data(results=filtered, page=0)
    await show_place(msg, state)

# Helper: Show one place with pagination
async def show_place(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    results = data["results"]
    page = data.get("page", 0)

    place = results[page]
    text = (
        f"📌 *{place['name']}* in *{place['city']}*\n"
        f"🧾 {place['description']}\n"
        f"📍 {place['location']}\n"
        f"🏷️ Tags: {', '.join(place['tags'])}\n"
        f"📂 Category: {place['category']}\n"
        f"📄 {page + 1} of {len(results)}"
    )

    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Prev", callback_data="prev"))
    if page < len(results) - 1:
        buttons.append(InlineKeyboardButton(text="Next ➡️", callback_data="next"))

    markup = InlineKeyboardMarkup(inline_keyboard=[buttons]) if buttons else None
    await msg.answer(text, reply_markup=markup, parse_mode="Markdown")

# Pagination handler
@router.callback_query(F.data.in_({"next", "prev"}))
async def paginate(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 0)
    if call.data == "next":
        page += 1
    elif call.data == "prev":
        page -= 1

    await state.update_data(page=page)
    await call.message.delete()
    await show_place(call.message, state)
