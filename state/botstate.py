from aiogram.filters.state import StatesGroup, State


class BotState(StatesGroup):
    audio_uri = State()
    video_uri = State()