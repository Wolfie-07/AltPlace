# states/filter.py

from aiogram.fsm.state import StatesGroup, State

class FilterPlace(StatesGroup):
    city = State()
    category = State()
    tags = State()
    results = State()  # stores list of places
    page = State()     # stores current index
