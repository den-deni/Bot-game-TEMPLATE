from aiogram import F, Router
from aiogram.types import CallbackQuery

from motor.core import AgnosticDatabase as MDB

callback_roter = Router()

@callback_roter.callback_query(F.data == 'profile')
async def get_profile(call: CallbackQuery, db: MDB):
    pass