from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from motor.core import AgnosticDatabase as MDB

from keyboard.builder_kb import builder_keyboard


points_router = Router()


@points_router.callback_query(F.data == 'exchanger')
async def get_exchanger(call: CallbackQuery, db: MDB):
    user = await db.profile2.find_one(
        {"_id": call.from_user.id}
    )
    points = user['points']
    if points < 1000:
        await call.answer('1 💎 = 1000 points\nВтебе не достатьно points грай далі та вигравай', show_alert=True)
    else:
        await call.message.edit_text(text=f"{hbold('Бажаєш придбати 💎')}", reply_markup=builder_keyboard(
            ['Купити 💎', 'Назад⬅️'],
            ['bay', 'back'],
            sizes=2
        )
    )
        
@points_router.callback_query(F.data == 'bay')
async def bay_diamond(call: CallbackQuery, db: MDB):
    user = await db.profile2.find_one(
        {"_id": call.from_user.id}
    )
    balance = user['points']
    if balance >= 1000:
        await db.profile2.update_one(
            {"_id": call.from_user.id},
            {"$inc": {'points': -1000,
                      "diamond": 1},
            }
        )
        await call.answer('Ти бридбав 1 💎\n -1000 points', show_alert=True)
    else:
        await call.answer('Невистачає points', show_alert=True)
