import asyncio
import logging

from multiprocessing import Process
from aiogram import Dispatcher
from aiogram.methods import DeleteWebhook

from bot import mybot
from commands.handlers import handlers_router
from commands.common import common_router
from commands.admin_handlers import admin_router
from database.models import async_main
from database.requests import users_for_notification
from texts import push


dp = Dispatcher()
dp.include_router(admin_router)
dp.include_router(common_router)
dp.include_router(handlers_router)


# async def send_mes():
#     users = await users_for_notification()
#     if users:
#         for user in users:
#             await mybot.send_message(chat_id=user.tg_id, text=push)
#             await asyncio.sleep(1)


# async def scheduler():
#     while True:
#         await send_mes()
#         await asyncio.sleep(432000)


# def worker():
#     asyncio.run((scheduler()))


async def main():
    await async_main()
    # process = Process(target=worker)
    # process.start()
    logging.basicConfig(level=logging.INFO)
    await mybot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(mybot)
    # process.join()


if __name__ == "__main__":
    asyncio.run(main())
