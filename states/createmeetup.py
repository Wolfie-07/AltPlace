from aiogram.fsm.state import StatesGroup, State

class CreateMeetup(StatesGroup):
    title = State()
    description = State()
    location = State()
    city = State()
    event_date = State()
    time = State()
    confirm = State()
