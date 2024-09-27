from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import LinkPreviewOptions

import texts
from database.requests import set_user, get_task_and_answer_2, get_random_task, check_user, update_user_info
from keyboards import get_start_keyboard, get_task_keyboard, first_part_keyboard, second_part_keyboard
from texts import *

handlers_router = Router()


class ExamTask(StatesGroup):
    part_choice = State()
    check_password = State()
    question = State()
    answer = State()


@handlers_router.message(F.text == texts.start_action_button)
async def back_to_work(message: types.Message, state: FSMContext):
    user_info = message.from_user
    await message.answer(text=texts.menu_text, reply_markup=get_start_keyboard())
    await update_user_info(user_info.id)
    await state.set_state(ExamTask.part_choice)


@handlers_router.message(F.text.lower().contains('меню'))
async def handle_menu(message: types.Message, state: FSMContext):
    user_info = message.from_user
    await message.answer(text=texts.menu_text, reply_markup=get_start_keyboard())
    await state.set_state(ExamTask.part_choice)


@handlers_router.message(F.text == texts.first_part_button)
async def first_part_cmd(message: types.Message, state: FSMContext):
    user_info = message.from_user
    await message.answer(text=texts.first_part_text, reply_markup=first_part_keyboard())
    await update_user_info(user_info.id)
    await state.set_state(ExamTask.question)


@handlers_router.message(F.text == texts.second_part_button)
async def first_part_cmd(message: types.Message, state: FSMContext):
    user_info = message.from_user
    await message.answer(text=texts.second_part_text, reply_markup=second_part_keyboard())
    await update_user_info(user_info.id)
    await state.set_state(ExamTask.question)


@handlers_router.message(F.text == 'Нет, пойду отдыхать ☺️')
async def handle_reject(message: types.Message, state: FSMContext):
    await message.answer(text=texts.goodbye)
    await state.clear()


@handlers_router.message(ExamTask.question)
async def handle_task(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    task_number = message.text.split()[-1]
    if task_number in NUMBERS_FIRST_PART:
        task_and_answer = await get_task_and_answer_2(user_id, task_number)
        print(task_and_answer.answer)
        await message.answer(text=task_and_answer.task, reply_markup=get_task_keyboard(task_number))
        # await message.answer_photo(photo=types.FSInputFile(task_and_answer.path), reply_markup=get_task_keyboard(task_number))
        if task_and_answer.image:
            await message.answer_photo(photo=task_and_answer.image,
                                       reply_markup=get_task_keyboard(task_number))
        # await message.answer_photo(photo=task_and_answer.link, reply_markup=get_task_keyboard(task_number))
        await state.update_data(answer=task_and_answer.answer, num=task_number)
        await state.set_state(ExamTask.answer)
    elif task_number in NUMBERS_SECOND_PART:
        task_and_answer = await get_task_and_answer_2(user_id, task_number)
        print(task_and_answer.answer)
        await message.answer(text=task_and_answer.task, reply_markup=get_task_keyboard(task_number))
        if task_and_answer.image:
            await message.answer_photo(photo=task_and_answer.image,
                                       reply_markup=get_task_keyboard(task_number))
        # await message.answer_photo(photo=types.FSInputFile(task_and_answer.path), reply_markup=get_task_keyboard(task_number))
        # await message.answer_photo(photo=task_and_answer.link, reply_markup=get_task_keyboard(task_number))
        await state.update_data(answer=task_and_answer.answer, source=task_and_answer.source, num=task_number)
        await state.set_state(ExamTask.answer)
    else:
        await message.answer(text=texts.incorrect_message,
                             reply_markup=get_start_keyboard())


@handlers_router.message(ExamTask.answer)
async def check_answer(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data['num'])
    if str(message.text) == user_data['answer'] and user_data['num'] in NUMBERS_FIRST_PART:
        await message.answer(text=texts.congrats,
                             reply_markup=get_task_keyboard(user_data['num']))
    if str(message.text) != user_data['answer'] and user_data['num'] in NUMBERS_FIRST_PART:
        await message.answer(text=f"{texts.wrong_answer} {user_data['answer']}\n"
                                  f"{texts.solve_more_message}", reply_markup=get_task_keyboard(user_data['num']))
    if str(message.text) and user_data['num'] in NUMBERS_SECOND_PART:
        await message.answer(text=f"{user_data['answer']}\n"
                                  f"{user_data['source']}\n\n"
                                  f"{texts.solve_more_message}", reply_markup=get_task_keyboard(user_data['num']))
    await state.set_state(ExamTask.question)


@handlers_router.message()
async def handle_all(message: types.Message):
    await message.answer(text=unexpected_message)
