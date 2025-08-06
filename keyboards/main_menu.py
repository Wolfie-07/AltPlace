from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☕️ Cafes"),
            KeyboardButton(text="🏛 Libraries"),
            KeyboardButton(text="🏢 Venues")
        ],
        [
            KeyboardButton(text="📅 My_Meetups"),
            KeyboardButton(text="📅 Meetups"),
            KeyboardButton(text="➕ Create Meetup")
        ],
        [
            KeyboardButton(text="📝 Suggest"),
            KeyboardButton(text="👤 Profile"),
            KeyboardButton(text="📞 Contact")
        ],
        [
            KeyboardButton(text="🔍 Filter"),
            KeyboardButton(text="❓ Help")
        ]
    ],
    resize_keyboard=True
)
