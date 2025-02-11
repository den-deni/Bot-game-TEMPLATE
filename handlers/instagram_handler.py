import os

from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.markdown import hbold
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from motor.core import AgnosticDatabase as MDB

from state.botstate import BotState
from utils.dowload_utils import load_insta_pic
from cleaning.cleaner import delete_non_images, get_single_image_from_folder


insta_router = Router()

@insta_router.callback_query(F.data == 'insta')
async def start_proces_insta(call: CallbackQuery, db: MDB, state: FSMContext):
    user = await db.profile2.find_one({"_id": call.from_user.id})
    balance = user['diamond']
    if balance <= 0:
        await call.answer(text='Не достатьньо 💎! Грай щоб заробити', show_alert=True)
    else:
        await call.message.answer(text=f"{hbold('Ок відправ нікнейм чиє фото профілю треба:')}")
        await call.answer()
        await state.set_state(BotState.insta_uri)


@insta_router.message(BotState.insta_uri)
async def get_insta_uri(message: Message, bot: Bot, state: FSMContext, db: MDB):
    uri = message.text
    load_insta_pic(prof=uri)
    delete_non_images(folder_path='static/instapic')
    pic = get_single_image_from_folder(folder_path='static/instapic')
    photo = FSInputFile(path=pic)
    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=uri, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Меню', callback_data='menu')
            ]
        ]
    )
)
    await db.profile2.update_one({"_id": message.from_user.id}, {"$inc": {'diamond': -1}})
    os.remove(pic)
    await state.clear()

    
