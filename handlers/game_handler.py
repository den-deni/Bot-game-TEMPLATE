import asyncio

from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold
from aiogram.enums import DiceEmoji

from motor.core import AgnosticDatabase as MDB

from keyboard.builder_kb import builder_keyboard
from state.botstate import DiceGame
from utils.game_utils import get_card, calculate_score, get_dict


game_router = Router()



# блок ігра в кубік

@game_router.callback_query(F.data == 'dicegame')
async def start_state_game(call: CallbackQuery, bot: Bot, db: MDB, state: FSMContext):
        bot_roll = await bot.send_dice(chat_id=call.message.chat.id, emoji=DiceEmoji.DICE)
        bot_value = bot_roll.dice.value
        await db.dicegame.update_one(
             {"_id": call.from_user.id},
             {"$set": {'botvalue': bot_value}},
             upsert=True
        )
        await call.message.answer('Натисни на кубік 👆')
        await call.answer()
        await state.set_state(DiceGame.user_value)
        
@game_router.message(DiceGame.user_value)       
async def move_user(message: Message, db: MDB, state: FSMContext):
            if message.dice:
                user_value = message.dice.value
                await asyncio.sleep(3)
                game = await db.dicegame.find_one({"_id": message.from_user.id})
                bot_value = game['botvalue']
                
                if user_value > bot_value:
                    await db.profile2.update_one({"_id": message.from_user.id},
                                                {
                                                    "$inc": {"points": 30}
                                                })
                    await message.answer("Ти виграв 🎉 30 points", reply_markup=builder_keyboard(
                        text=["Кинути ще🎲", "Меню ігри", "Назад в меню⬅️"],
                        callback=["dicegame", "game", "back"],
                        sizes=2
                        )
                    )
                elif user_value < bot_value:
                    await message.answer("Бот виграв! 🤖", reply_markup=builder_keyboard(
                        text=["Кинути ще🎲", "Меню ігри", "Назад в меню⬅️"],
                        callback=["dicegame", "game", "back"],
                        sizes=2
                        )
                    )
                else:
                    await message.answer("Нічія! 🤝", reply_markup=builder_keyboard(
                        text=["Кинути ще🎲", "Меню ігри", "Назад в меню⬅️"],
                        callback=["dicegame", "game", "back"],
                        sizes=2
                        )
                    )
                await state.clear()
                
            else:
                 await message.answer('Щоб зробити хід натисни на кубік')
                 return

            await db.dicegame.delete_one({"_id": message.from_user.id})

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

        await call.message.edit_text(f"{hbold('Карти бота:')}\n{bot_str}\n{hbold('Всього:')}{dealer_score}")

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
            ['⬆️', '⬇️', "Меню ігри", 'Назад⬅️'],
            ['up', 'down', "game", 'back'],
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
            await call.answer(text='Ти виграв +100 points🎉', show_alert=True)
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
            await call.answer(text='Ти програв☹️', show_alert=True)

    elif call.data == 'down':
        if price < userprice:
            await call.message.edit_reply_markup(reply_markup=builder_keyboard(
                ['BitCoin💸', 'Назад⬅️'],
                ['playbitcoin', 'back'],
                sizes=2
            )
        )
            await call.answer(text='Ти виграв 100 points🎉', show_alert=True)
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
            await call.answer(text='Ти програв☹️', show_alert=True)

    await db.gamecoin.delete_one(
                {"_id": call.from_user.id}
            )