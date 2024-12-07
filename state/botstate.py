from aiogram.filters.state import StatesGroup, State


class BotState(StatesGroup):
    audio_uri = State()
    video_uri = State()
    insta_uri = State()



class DiceGame(StatesGroup):
    user_value = State()
    bot_value = State()