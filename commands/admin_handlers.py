import asyncio

from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, or_f
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime as dt
from keyboards import yes_no, send_or_not

from bot import mybot
from database.requests import delete_user, show_all_users, check_user, users_for_notification,update_notification_info
from texts import push

admin_router = Router()


class AdminOperations(StatesGroup):
    user_delete = State()
    report_sending = State()
    send_notification = State()
    send_message = State()
    check_message = State()


@admin_router.message(Command('show_all_users'))
async def all_users(message: types.Message, state: FSMContext):
    user_info = message.from_user
    if user_info.id == 1973820682 or user_info.id == 933536479:
        users = await show_all_users()
        table = f"ID | tg_id | Username | Регистрация | Последний вход | Дата оповещения\n"
        for user in users:
            print(user.id)
            # delta = int(str(user.last_enter - dt.now())[:2]) + 1
            table += f"{user.id} - {user.tg_id} - @{user.username} - {user.created} - {user.last_enter} - {user.last_notification}\n"
        await message.answer(table)
    else:
        await message.answer(text='Эта функция доступна только для админа')
        await state.clear()


@admin_router.message(Command('need_notification'))
async def notification_cmd(message: types.Message, state: FSMContext):
    user_info = message.from_user
    if user_info.id == 1973820682 or user_info.id == 933536479:
        users = await users_for_notification()
        if users:
            table = f"tg_id | Username | Последний вход | Дней с последнего входа | Дата оповещения\n"
            for user in users:
                table += f"{user.tg_id} - @{user.username} - {user.last_enter} - " \
                         f"{(dt.now() - user.last_enter).days} дней - {user.last_notification}\n"
            await message.answer(table, parse_mode=ParseMode.HTML)
            await message.answer(text='Отправим рассылку по отстающим ученика?', reply_markup=yes_no())
            await state.set_state(AdminOperations.send_notification)
        else:
            await message.answer(text='Нет учеников, которые не заходили более 5 дней')
    else:
        await message.answer(text='Эта функция доступна только для админа')
        await state.clear()


@admin_router.message(AdminOperations.send_notification)
async def send_cmd(message: types.Message, state: FSMContext):
    user_info = message.from_user
    if user_info.id == 1973820682 or user_info.id == 74395999 or user_info.id == 1113517153: #первый мой
        users = await users_for_notification()
        if message.text == 'Да':
            for user in users:
                await mybot.send_message(chat_id=user.tg_id,
                                         text=push)
                await update_notification_info(user.tg_id)
                await asyncio.sleep(1)
                await message.answer(text=f'Сообщение пользователю {user.tg_id} успешно отправлено')
            await state.clear()
        elif message.text == 'Пока нет':
            await message.answer(text='Окей, пока не будем отправлять сообщения!')
            await state.clear()
        else:
            await message.answer(text='Не понял сообщение! Попробуй еще раз!', reply_markup=yes_no())
            await state.set_state(AdminOperations.send_notification)
    else:
        await message.answer(text='Эта функция доступна только для админа')
        await state.clear()


@admin_router.message(Command('delete'))
async def delete_cmd(message: types.Message, state: FSMContext):
    user_info = message.from_user
    if user_info.id == 1973820682 or user_info.id == 74395999 or user_info.id == 1113517153:
        await message.answer(text='Отправьте telegram_id пользователя, которого нужно удалить')
        await state.set_state(AdminOperations.user_delete)
    else:
        await message.answer(text='Эта функция доступна только для админа')
        await state.clear()


@admin_router.message(AdminOperations.user_delete)
async def delete_user_cmd(message: types.Message, state: FSMContext):
    user_info = message.from_user
    if user_info.id == 1973820682 or user_info.id == 74395999 or user_info.id == 1113517153:
        tg_id = message.text
        user = await check_user(tg_id)
        if user:
            await delete_user(tg_id)
            await message.answer(text=f'Пользователь {tg_id} успешно удален')
        else:
            await message.answer(text=f'id введен некорректно либо не существует, проверьте еще раз')
    else:
        await message.answer(text='Эта функция доступна только для админа')
    await state.clear()


@admin_router.message(or_f(Command('send_message'), F.text == 'Поменять сообщение'))
async def prepare_message_cmd(message: types.Message, state: FSMContext):
    user_info = message.from_user
    if user_info.id == 1973820682 or user_info.id == 74395999 or user_info.id == 1113517153:
        users = await show_all_users()
        if users:
            await message.answer(text='Давай отправим рассылку по ученикам\n\n'
                                      'Отправь, пожалуйста, сообщение, которое нужно отправить')
            await state.set_state(AdminOperations.check_message)
        else:
            await message.answer(text='Не удалось получить список пользователей :(')
    else:
        await message.answer(text='Эта функция доступна только для админа')
        await state.clear()


@admin_router.message(AdminOperations.check_message)
async def check_message(message: types.Message, state: FSMContext):
    user_info = message.from_user
    if user_info.id == 1973820682 or user_info.id == 74395999 or user_info.id == 1113517153:
        await message.answer(text='Проверь, пожалуйста, твое сообщение для рассылки', reply_markup=send_or_not())
        await message.answer(text=message.text)
        await state.update_data(message_for_send=message.text)
        await state.set_state(AdminOperations.send_message)
    else:
        await message.answer(text='Эта функция доступна только для админа')
        await state.clear()


@admin_router.message(AdminOperations.send_message)
async def send_cmd(message: types.Message, state: FSMContext):
    user_info = message.from_user
    user_data = await state.get_data()
    await state.clear()
    print(user_data)
    if user_info.id == 1973820682 or user_info.id == 74395999 or user_info.id == 1113517153:
        users = await show_all_users()
        if message.text == 'Отправляем рассылку, все хорошо':
            for user in users:
                try:
                    await mybot.send_message(chat_id=user.tg_id,
                                             text=user_data['message_for_send'])
                    await asyncio.sleep(1)
                    await message.answer(text=f'Сообщение пользователю {user.tg_id} успешно отправлено')
                except:
                    await message.answer(text=f'Сообщение пользователю {user.tg_id} не доставлено')
            await state.clear()
        elif message.text == 'Поменять сообщение':
            await state.clear()
        elif message.text == 'Выйти':
            await message.answer(text=f'До скорого!')
            await state.clear()
        else:
            await message.answer(text='Не понял сообщение! Попробуй еще раз!', reply_markup=send_or_not())
            await state.set_state(AdminOperations.send_message)
            print(user_data)
    else:
        await message.answer(text='Эта функция доступна только для админа')
        await state.clear()
