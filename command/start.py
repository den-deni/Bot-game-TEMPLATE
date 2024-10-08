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
@router.callback_query(F.data == 'back')
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
                    "points": 0,
                    "diamond": 0,
                    "game": {"count": 3, "time": None},
                    "price": {"audio": 1, "video": 1, "photo": 1, "insta": 1},

                }
            )
            await db.profile2.update_one(
                {"_id": message.from_user.id},
                {"$inc": {'diamond': 1}}
            )
            await message.answer(f"{hbold('Привіт, гравцю! 🎉')}\n"
                                 f"{hbold('Вітаю тебе! Як перший користувач, ти отримуєш бонус — 1 діамант 💎!')}\n"
                                 f"{hbold('Використовуй його, щоб завантажити свій перший контент або накопичуй більше діамантів, граючи в ігри.')}\n"
                                 f"{hbold('Починай грати прямо зараз і отримуй ще більше призів! 🚀')}\n"
                                 f"{hbold('Удачі та приємної гри! 🎮')}")

    pattern = dict(
        text=f"{hbold('Головне меню бота 🤖')}",
        reply_markup=builder_keyboard(
            text=["Профіль👤", "🎮", "🤖", "💎", "Про бота📜"],
            callback=["profile", "game", "shop", "exchanger", "support"],
            sizes=2
        )
    )
    if isinstance(message, CallbackQuery):
        await message.message.edit_text(**pattern)
        await message.answer()
    else:
        await message.answer(**pattern)
