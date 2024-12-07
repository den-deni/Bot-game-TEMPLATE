import time
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from motor.core import AgnosticDatabase as MDB

from keyboard.builder_kb import builder_keyboard

time_router = Router()


# блок для обробки кнопки таймер
@time_router.callback_query(F.data == 'timer')
async def start_timer(call: CallbackQuery, db: MDB):
    user = await db.profile2.find_one({"_id": call.from_user.id})
    count_game = user["game"]["count"]
    timer_game = user["game"]["time"]

    # Определяем текущее время
    current_time = datetime.now()
    reset_time = current_time + timedelta(seconds=120)
    await db.profile2.update_one({"_id": call.from_user.id}, {"$set": {'game.time': reset_time}})
    timer = await db.profile2.find_one({"_id": call.from_user.id})
    t = timer['game']['time']
    if current_time > reset_time:
        await call.message.answer(f"Таймер сброшен, вы можете продолжить.", reply_markup=builder_keyboard(
            ['Claim', 'Back'],
            ['claim', 'back'],
            sizes=2
        )
    )
        await db.profile2.update_one({"_id": call.from_user.id}, {"$inc": {'game.time': None}})
    else:
        await call.message.answer("no")
        await call.answer()




# def get_time():
#     data = datetime.now()
#     time = data.time()
#     current_time = time.strftime("%H:%M:%S")
#     print(current_time)

# get_time()