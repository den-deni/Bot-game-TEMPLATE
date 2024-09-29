import asyncio
import logging
import os
import sys

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase as MDB

from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode




async def main() -> None:
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    cluster = AsyncIOMotorClient(host="localhost", port=27017)
    db = cluster.gamebotdb
    dp = Dispatcher()
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
