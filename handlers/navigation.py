from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hlink, hbold

from motor.core import AgnosticDatabase as MDB

from keyboard.builder_kb import builder_keyboard


navigation_router = Router()

@navigation_router.callback_query(F.data == 'profile')
async def get_profile(call: CallbackQuery, db: MDB):
    user = await db.profile2.find_one(
        {
            "_id": call.from_user.id
        }
    )
    await call.message.edit_text(
        f"{hbold('ID')}....{call.from_user.id}\n"
        f"{hbold('Name')}....{call.from_user.full_name}\n\n"
        f"{hbold('Points')}....{user['points']}\n"
        f"{hbold('Diamond')}....{user['diamond']}💎",
        reply_markup=builder_keyboard(
            text=['Назад в меню ⬅️'],
            callback=['back'],
            sizes=1
        )
    )

@navigation_router.callback_query(F.data == 'game')
async def get_profile(call: CallbackQuery):
    await call.message.edit_text(text=f"{hbold('Меню ігри')}", reply_markup=builder_keyboard(
        text=["Black_Jack🃏", "Dice🎲", "BitCoin💸", "Таймер⏱️", "Назад в меню⬅️"],
        callback=["blackjack", "dice", "bitcoin", "timer", "back"],
        sizes=2
    )
)
    await call.answer()


@navigation_router.callback_query(F.data == "dice")
async def get_cubs(call: CallbackQuery):
    await call.message.edit_text(text=f"{hbold('Гра в кубік Dice')}\n"
                                 f"{hbold('Перший кубік бота')}\n"
                                 f"{hbold('У кого більше той переміг')}\n"
                                 f"{hbold('Одна перемога +30 points')}",reply_markup=builder_keyboard(
        text=["Play🎲", "Назад ⬅️"],
        callback=["dicegame", "game"],
        sizes=2
        )
    )
    await call.answer()



@navigation_router.callback_query(F.data == 'blackjack')
async def get_cards_start(call:CallbackQuery):
    await call.message.edit_text(text=f"{hbold('Гра BlackJack')}\n"
                                      f"{hbold('Хто набрав більше переміг')}\n"
                                      f"{hbold('Більше 21 програв')}\n"
                                      f"{hbold('J, Q, K рахуються як 10')}\n"
                                      f"{hbold('A рахується 11 якщо загальна сума очок у руці не перевищує 21')}\n"
                                      f"{hbold('A рахується як 1, якщо сума очок з урахуванням А як 11 призводить до перебору (сума більше 21)')}\n"
                                      f"{hbold('Цифри рахуються як є')}\n"
                                      f"{hbold('Одна перемога +50 points')}\n", reply_markup=builder_keyboard(
                                          ['Play🃏', 'Назад⬅️'],
                                          ['playjack', 'game'],
                                          sizes=2
                                      )
                                    )
    

@navigation_router.callback_query(F.data == 'bitcoin')
async def get_start_bitcoin(call: CallbackQuery):
    await call.message.edit_text(text=f"{hbold('Гра BitCoin')}\n"
                                 f"{hbold('Потрібно вгадати куди піде ціна Bitcoin')}\n"
                                 f"{hbold('Один виграш +100 points')}\n", reply_markup=builder_keyboard(
                                     ['Play📊', 'Назад⬅️'],
                                     ['playbitcoin', 'game'],
                                     sizes=2
                                 )
                                )
    

@navigation_router.callback_query(F.data == 'shop')
async def get_shop(call: CallbackQuery):
    await call.message.edit_text(text=f"{hbold('Вітаю в BotShop')}\n"
                                      f"{hbold('Тут ти можеш витратити свої 💎')}\n"
                                      f"{hbold('Вибери що потрібно 👇')}", reply_markup=builder_keyboard(
                                        ['Youtube/audio', 'Youtube/video', 'Insta/pic', 'Назад⬅️'],
                                        ['audio', 'video', 'insta', 'back'],
                                        sizes=1
                                    )
                                )
                                    
@navigation_router.callback_query(F.data == 'support')
async def get_support(call: CallbackQuery):
    await call.message.edit_text(text=f"{hbold('Бот надає можливість завантажувати файли з YouTube або Instagram, але для цього користувачам потрібно грати в ігри')}\n"
                                      f"{hbold('За виграш у іграх користувачі заробляють поінти, які можна накопичувати')}\n"
                                      f"{hbold('Зібрані поінти можна обміняти на діаманти — внутрішню валюту бота')}\n"
                                      f"{hbold('Користувач може використовувати діаманти для завантаження потрібного контенту з YouTube або Instagram')}\n"
                                      f"{hbold('Чим більше виграє користувач, тим більше контенту він зможе завантажити.')}\n"
                                      f"{hbold('Виникли питання або побачив баг пиши')}👇\n"
                                      f"{hlink(title='SupportBot', url='https://t.me/su_rwx')}\n"
                                      f"{hbold('P.S: За інфо бонус 💎')}", reply_markup=InlineKeyboardMarkup(
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text='Зрозуміло ✔️', callback_data='back')
                                              ]
                                          ]
                                      )
                                    )
    