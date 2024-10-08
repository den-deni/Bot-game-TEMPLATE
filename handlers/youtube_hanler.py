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
from utils.dowload_utils import load_audio, load_video


yt_router = Router()

# блок для завантаження аудіо

@yt_router.callback_query(F.data == 'audio')
async def get_audio_file(call: CallbackQuery, db: MDB, state: FSMContext):
    user = await db.profile2.find_one(
        {"_id": call.from_user.id}
    )
    diamond = user['diamond']
    if diamond <= 0:
        await call.answer(text='Не достатьньо 💎! Грай щоб заробити', show_alert=True)

    else:
        await call.message.edit_text(text=f"{hbold('Придбати одне завантаження musik файлу за 1💎')}\n"
                                          f"{hbold('Відправ боту посилання')}\n"
                                          f"{hbold('Посилання може бути з Youtube  або YoutubMusic')}\n"
                                          f"{hbold('Попередження файл  до 50мб')}\n"
                                          f"{hbold('Для відміни 👉 /cancel')}")
        await state.set_state(BotState.audio_uri)
        await call.answer()



@yt_router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(text=f"{hbold('Відмінено')}", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Меню', callback_data='back')
            ]
        ]
    )
)



@yt_router.message(BotState.audio_uri)
async def send_audio_file(message: Message, db: MDB, bot: Bot, state: FSMContext):
    try:
        if message.text.startswith(('https://music.youtube', 'https://youtube', 'https://youtu.be')):
            file = load_audio(url=message.text)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer(text=f"{hbold('🫡Починаю завантаження зачакай кілька хвилин')}")
            audio = FSInputFile(path=file)
            async with ChatActionSender.upload_document(chat_id=message.chat.id, bot=bot):
                await bot.send_audio(chat_id=message.chat.id, audio=audio)
                await message.answer(f"{hbold('Завантаження закінчено')}", reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text='Назад⬅️', callback_data='back')
                        ]
                    ]
                )
            )
                await db.profile2.update_one(
                    {"_id": message.from_user.id},
                    {"$inc": {'diamond': -1}}
                )

                await state.clear()
        else:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer(text=f"{hbold('Не правильне посилання, відправ знову')}", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Назад', callback_data='back')
                    ]
                ]
            )
        )
            return
    except Exception:
        await message.answer(text=f"{hbold('Час запиту минув спробуй ще раз🧭')}", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Update🔁', callback_data='audio'),
                    InlineKeyboardButton(text='Exit', callback_data='back')
                ]
            ]
        )
    )
    finally:
        file_path = file
        os.remove(file_path)

# блок для завантаження відео

@yt_router.callback_query(F.data == 'video')
async def get_audio_file(call: CallbackQuery, db: MDB, state: FSMContext):
    user = await db.profile2.find_one(
        {"_id": call.from_user.id}
    )
    diamond = user['diamond']
    if diamond <= 0:
        await call.answer(text='Не достатьньо 💎! Грай щоб заробити', show_alert=True)

    else:
        await call.message.edit_text(text=f"{hbold('Придбати одне завантаження video short файлу за 1💎')}"
                                          f"{hbold('Відправ боту посилання')}\n"
                                          f"{hbold('Посилання може бути з Youtube')}\n"
                                          f"{hbold('Попередження бот завантажуе тільки short video')}"
                                          f"{hbold('Для відміни 👉 /cancel')}")
        await state.set_state(BotState.video_uri)
        await call.answer()




@yt_router.message(BotState.video_uri)
async def send_audio_file(message: Message, db: MDB, bot: Bot, state: FSMContext):
    try:
        if message.text.startswith(('https://youtube.com/shorts')):
            file = load_video(url=message.text)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer(text=f"{hbold('🫡Починаю завантаження зачакай кілька хвилин')}")
            video = FSInputFile(path=file)
            async with ChatActionSender.upload_video(chat_id=message.chat.id, bot=bot):
                await bot.send_video(chat_id=message.chat.id, video=video)
                await message.answer(f"{hbold('Завантаження закінчено')}", reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text='Назад⬅️', callback_data='back')
                        ]
                    ]
                )
            )
                await db.profile2.update_one(
                    {"_id": message.from_user.id},
                    {"$inc": {'diamond': -1}}
                )
                await state.clear()
                
        else:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer(text=f"{hbold('Не правильне посилання, відправ знову')}", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Назад', callback_data='back')
                    ]
                ]
            )
        )
            return
    except Exception:
        await message.answer(text=f"{hbold('Час запиту минув спробуй ще раз🧭')}", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Update🔁', callback_data='audio'),
                    InlineKeyboardButton(text='Exit', callback_data='back')
                ]
            ]
        )
    )
    finally:
            file_path = file
            os.remove(file_path)
       

