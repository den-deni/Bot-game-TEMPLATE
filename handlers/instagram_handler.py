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
from temp import delete_non_images


insta_router = Router()

@insta_router.callback_query(F.data == 'insta')
async def start_proces_insta(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text='send me nikname insta')
    await call.answer()
    await state.set_state(BotState.insta_uri)


@insta_router.message(BotState.insta_uri)
async def get_insta_uri(message: Message, bot: Bot, state: FSMContext, db: MDB):
    uri = message.text
    load_insta_pic(prof=uri)
    delete_non_images(folder_path='static/instapic')
    
    await bot.send_photo(chat_id=message.chat.id, photo='static/instapic')
    await state.clear()

    
