from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from middleware.adminfilter import AdminCheck
from motor.core import AgnosticDatabase as MDB
from keyboard.builder_kb import builder_keyboard

admin_router = Router()

admin_router.message.middleware(AdminCheck())
@admin_router.message(Command('root'))
async def get_admin_panel(message: Message):
    await message.answer(text='Hello world', reply_markup=builder_keyboard(
        ['User list', 'Admin list', 'Розсилка бот', 'Pозсилка канал'],
        ['user', 'admins', 'senderbot', 'senderchanel'],
        sizes=2
    )
)
admin_router.callback_query.middleware(AdminCheck())
@admin_router.callback_query(F.data == 'user')
async def get_user_list(call: CallbackQuery, db: MDB):
    users_cursor = db.profile2.find({}, {"_id": 1, "name": 1})  # Извлекаем ID и имена пользователей
    user_info = []

    async for user in users_cursor:  # Асинхронный цикл для перебора курсора
        user_info.append(f"ID: {user['_id']}, Name: {user['name']}")

    # Отправляем пользователю список имен и ID
    await call.message.answer(text="\n".join(user_info) if user_info else "Нет пользователей.", reply_markup=builder_keyboard(
        ['Back', 'Message'],
        ['back', 'message'],
        sizes=2
    ))
    await call.answer()


@admin_router.callback_query(F.data == 'senderbot')
async def get_bot_send(call: CallbackQuery, bot: Bot):
    ...


@admin_router.callback_query(F.data == 'senderchanel')
async def get_chanel_send(call: CallbackQuery, bot: Bot):
    ...

