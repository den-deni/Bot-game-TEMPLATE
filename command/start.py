from contextlib import suppress

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.utils.markdown import hbold

from motor.core import AgnosticDatabase as MDB
from pymongo.errors import DuplicateKeyError

from keyboard.builder_kb import builder_keyboard

router = Router()

@router.message(Command('start'))
@router.callback_query(F.data == 'mainmenu')
async def get_start(message: Message | CallbackQuery, db: MDB):
    user = await db.profile2.find_one(
        {
            "_id": message.from_user.id
        }
    )
    if user is None:
        with suppress(DuplicateKeyError):
            await db.profile2.insert_one(
                {
                    "_id": message.from_user.id,
                    "name": message.from_user.full_name,
                    "balance": 0,
                    "points": 0,
                    "diamond": 0,
                    "game": {"count": 3, "time": None, "win": 0},
                    "price": {"d1": 100, "d2": 200, "d3": 300, "audio": 1, "video": 2, "number": 1}
                }
            )
    pattern = dict(
        text=f"{hbold('>_text')}",
        reply_markup=builder_keyboard(
            text=["Профіль👤", "Грати🎮", "Магазин💳", "Обміник💎", "Підтримка⚙️"],
            callback=["profile", "game", "shop", "exchanger", "support"],
            sizes=2
        )
    )
    if isinstance(message, CallbackQuery):
        await message.message.edit_text(**pattern)
        await message.answer()
    else:
        await message.answer(**pattern)
