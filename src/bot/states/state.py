from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    waiting_telegram_id = State()
