import asyncio

from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.enums import DiceEmoji

from motor.core import AgnosticDatabase as MDB

from keyboard.builder_kb import builder_keyboard
from utils.game_utils import get_card, calculate_score, get_dict


game_router = Router()



# блок ігра в кубік

@game_router.callback_query(F.data == 'dicegame')
async def get_roll(call: CallbackQuery, bot: Bot, db: MDB):
        bot_roll = await bot.send_dice(chat_id=call.from_user.id, emoji=DiceEmoji.DICE)
        bot_value = bot_roll.dice.value
        await asyncio.sleep(4)

        user_roll = await bot.send_dice(chat_id=call.from_user.id, emoji=DiceEmoji.DICE)
        user_value = user_roll.dice.value
        await asyncio.sleep(4)

        if user_value > bot_value:
            await db.profile2.update_one({"_id": call.from_user.id},
                                        {
                                            "$inc": {"points": 30}
                                        })
            await call.message.answer("Ти виграв 🎉", reply_markup=builder_keyboard(
                 text=["Кинути ще🎲", "Назад в меню⬅️"],
                 callback=["dicegame", "back"],
                 sizes=2
                )
            )
            await call.answer(text="Ти виграв +30 points", show_alert=True)
        elif user_value < bot_value:
            await call.message.answer("Бот виграв! 🤖", reply_markup=builder_keyboard(
                 text=["Кинути ще🎲", "Назад в меню⬅️"],
                 callback=["dicegame", "back"],
                 sizes=2
                )
            )
            await call.answer()
        else:
            await call.message.answer("Нічія! 🤝", reply_markup=builder_keyboard(
                 text=["Кинути ще🎲", "Назад в меню⬅️"],
                 callback=["dicegame", "back"],
                 sizes=2
                )
            )
            await call.answer()

# блок ігра в 21

@game_router.callback_query(F.data == 'playjack')
async def get_jack(call: CallbackQuery, db: MDB):
     player_hand = [get_card(), get_card()]
     dealer_hand = [get_card(), get_card()]
     player_score = calculate_score(player_hand)

     await db.gamejack.update_one(
          {"_id": call.from_user.id},
          {"$set": {
               "player_hand": player_hand,
               "dealer_hand": dealer_hand,
               "player_score": player_score
          }
        },
          upsert=True
     )

     await call.message.edit_text(f"{hbold('Твої карти:')}\n"
                                  f"{player_hand[0]}\n"
                                  f"{player_hand[1]}\n"
                                  f"{hbold('Всього')}:{player_score}\n\n"
                                  f"{hbold('Карта бота')}\n"
                                  f"{dealer_hand[0]}", reply_markup=builder_keyboard(
                                       ['Ще', 'Пас'],
                                       ['hit', 'stand'],
                                       sizes=2
                                  )
                                )
     await call.answer()



@game_router.callback_query(F.data.in_({"hit", "stand"}))
async def handle_action(call: CallbackQuery, db: MDB):
    game = await db.gamejack.find_one({"_id": call.from_user.id})

    if not game:
        await call.message.answer("Гру не знайденно 🤷🏼‍♂️ тисни 👉 /start")
        return

    player_hand = game["player_hand"]
    dealer_hand = game["dealer_hand"]

    if call.data == "hit":
        # Игрок берет еще карту
        player_hand.append(get_card())
        player_score = calculate_score(player_hand)

        hand_str = '\n'.join(player_hand)
        


        await call.message.edit_text(f"{hbold('Твої карти:')}\n{hand_str}\n{hbold('Всього:')}{player_score}")
        await call.answer()

        # Обновляем данные в MongoDB
        await db.gamejack.update_one(
            {"_id": call.from_user.id},
            {"$set": {"player_hand": player_hand, "player_score": player_score}}
        )

        # Проверка на перебор
        if player_score > 21:
            await call.message.edit_text("Перебір! Ти програв", reply_markup=builder_keyboard(
                ['Play🃏', 'Меню ігри', 'Назад в меню⬅️'],
                ['playjack', 'game', 'back'],
                sizes=2
            )
        )
            await db.gamejack.delete_one({"_id": call.from_user.id})
            return

        # Предлагаем снова выбор
        await call.message.edit_text(f"{hbold('Твої карти:')}\n{hand_str}\n{hbold('Всього:')}{player_score}\n"
                                     "=====================\n"
                                    f"{hbold('Бажаєш взяти карту?')}\n",
                                    reply_markup=builder_keyboard(
                                    ['Ще', 'Пас'],
                                    ['hit', 'stand'],
                                    sizes=2
                                )
                            )

    elif call.data == "stand":
        # Ход дилера
        while calculate_score(dealer_hand) < 17:
            dealer_hand.append(get_card())

        dealer_score = calculate_score(dealer_hand)
        player_score = calculate_score(player_hand)

        bot_str = "\n".join(dealer_hand)

        await call.message.answer(f"{hbold('Карти бота:')}\n{bot_str}\n{hbold('Всього:')}{dealer_score}")

        # Определяем победителя
        if dealer_score > 21 or player_score > dealer_score:
            await call.message.answer(f"{hbold('Вітаю ти виграв!😀')}", reply_markup=builder_keyboard(
                ['Play🃏', 'Меню ігри', 'Назад в меню⬅️'],
                ['playjack', 'game', 'back'],
                sizes=2
            )
        )
            await db.profile2.update_one({"_id": call.from_user.id},
                {
                    "$inc": {"points": 50}
                }
            )
            await call.answer(text='Ти виграв +50 points', show_alert=True)
        elif player_score < dealer_score:
            await call.message.answer(f"{hbold('Ти програв😟')}", reply_markup=builder_keyboard(
                ['Play🃏', 'Меню ігри', 'Назад в меню⬅️'],
                ['playjack', 'game', 'back'],
                sizes=2
            )
        )
            await call.answer()
        else:
            await call.message.answer("Нічия🤝", reply_markup=builder_keyboard(
                ['Play🃏', 'Меню ігри', 'Назад в меню⬅️'],
                ['playjack', 'game', 'back'],
                sizes=2
            )
        )
            await call.answer()

        # Удаляем игру после завершения
        await db.gamejack.delete_one({"_id": call.from_user.id})


# блок ігра в біток
     
@game_router.callback_query(F.data == 'playbitcoin')
async def play_bitcoin(call: CallbackQuery, db: MDB):
    
        data = get_dict()
        name = data['index']
        price = data['price']
        await db.gamecoin.update_one(
            {"_id": call.from_user.id},
            {"$inc": {"userprice": price}},
        upsert=True
        )
        await call.message.edit_text(f"{hbold('Ціна BTC')}:{price}$\n"
                                     f"{hbold('Вибери куди піде ціна верх або вниз')}", reply_markup=builder_keyboard(
            ['⬆️', '⬇️', 'Назад⬅️'],
            ['up', 'down', 'back'],
            sizes=2
        )
    )
       
    


@game_router.callback_query(F.data.in_({'up', 'down'}))
async def choice_currency(call: CallbackQuery, db: MDB):
    data = get_dict()
    price = data['price']
    user = await db.gamecoin.find_one(
        {
            "_id": call.from_user.id
        }
    )
    userprice = user['userprice']

    if call.data == 'up':
        if price > userprice:
            await call.message.edit_reply_markup(reply_markup=builder_keyboard(
                ['BitCoin💸', 'Назад⬅️'],
                ['playbitcoin', 'back'],
                sizes=2
            )
        )
            await call.answer(text='Ти виграв +100 points', show_alert=True)
            await db.profile2.update_one(
                {"_id": call.from_user.id},
                {"$inc": {"points": 100}}
            )
        else:
            await call.message.edit_reply_markup(reply_markup=builder_keyboard(
                ['BitCoin💸', 'Назад⬅️'],
                ['playbitcoin', 'back'],
                sizes=2
            )
        )
            await call.answer(text=f'Ти програв\n{price}', show_alert=True)

    elif call.data == 'down':
        if price < userprice:
            await call.message.edit_reply_markup(reply_markup=builder_keyboard(
                ['BitCoin💸', 'Назад⬅️'],
                ['playbitcoin', 'back'],
                sizes=2
            )
        )
            await call.answer(text='Ти виграв 100 points', show_alert=True)
            await db.profile2.update_one(
                {"_id": call.from_user.id},
                {"$inc": {"points": 100}}
            )

        else:
            await call.message.edit_reply_markup(reply_markup=builder_keyboard(
                ['BitCoin💸', 'Назад⬅️'],
                ['playbitcoin', 'back'],
                sizes=2
            )
        )
            await call.answer(text=f'Ти програв\n{price}', show_alert=True)

    await db.gamecoin.delete_one(
                {"_id": call.from_user.id}
            )