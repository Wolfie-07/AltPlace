# states/suggest.py

from aiogram.fsm.state import StatesGroup, State

class SuggestPlace(StatesGroup):
    category = State()
    name = State()
    description = State()
    city = State()
    location = State()
    tags = State()
    confirm = State()
