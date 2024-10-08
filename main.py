import asyncio
import logging
import os
import sys

from motor.motor_asyncio import AsyncIOMotorClient


from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from command.start import router
from handlers.navigation import navigation_router
from handlers.game_handler import game_router
from handlers.youtube_hanler import yt_router
from handlers.points_handler import points_router



async def main() -> None:
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    cluster = AsyncIOMotorClient(host="localhost", port=27017)
    db = cluster.gamedb
    dp = Dispatcher()
    dp.include_routers(router, navigation_router, game_router, yt_router, points_router)
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
