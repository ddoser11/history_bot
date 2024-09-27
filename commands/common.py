from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from database.requests import check_user, update_user_info, set_user
from keyboards import get_start_keyboard, go
from commands.handlers import ExamTask
from texts import hello

common_router = Router()


@common_router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    user_info = message.from_user
    user = await check_user(user_info.id)
    if not user:
        await set_user(user_info.id, user_info.username)
    else:
        await update_user_info(user_info.id)
    await message.answer(text=hello,
                         parse_mode=ParseMode.HTML, reply_markup=go())
    await state.set_state(ExamTask.part_choice)
