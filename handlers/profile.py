from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text.in_({"/profile", "👤 Profile"}))
async def profile_command(message: types.Message):
    user = message.from_user
    profile_text = (
        f"👤 <b>Your Profile</b>\n\n"
        f"• Name: {user.full_name}\n"
        f"• Username: @{user.username if user.username else 'Not set'}\n"
        f"• Preferences: <i>Not set yet</i>\n\n"
        "📝 You’ll soon be able to customize your preferences!"
    )

    edit_profile_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Edit Profile (coming soon)", callback_data="edit_profile_placeholder")]
    ])

    await message.answer(profile_text, reply_markup=edit_profile_button, parse_mode="HTML")
@router.callback_query(F.data == "edit_profile_placeholder")
async def edit_profile_placeholder(call: types.CallbackQuery):
    await call.answer("This feature is coming soon! Stay tuned.")
    await call.message.edit_reply_markup()
    await call.message.answer("You can edit your profile preferences in the future. For now, you can explore other features of the bot!")