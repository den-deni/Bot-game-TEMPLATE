from typing import Any, Awaitable, Callable, Dict
from aiogram.filters import Filter
from aiogram import Bot, types
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, CallbackQuery

from config import ADMIN_ID


# перевірка на адміна бота
class AdminCheck(BaseMiddleware):
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if str(event.from_user.id) == ADMIN_ID:
            return await handler(event, data)  
        else:
            # Если это Message
            if isinstance(event, Message):
                await event.answer("Admin only!!!🔐")
            # Если это CallbackQuery
            elif isinstance(event, CallbackQuery):
                await event.answer("Admin only🔐")
            
            return 
        

# перевірка на тип чату 
class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types
    
# перевірка на адміна в групі
class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        user_chat = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        return user_chat.status in ['creator', 'administrator']