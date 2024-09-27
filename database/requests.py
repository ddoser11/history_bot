from database.models import async_session
from database.models import Task, User
from sqlalchemy import select,delete
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import ast


async def check_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user


async def users_for_notification():
    async with async_session() as session:
        current_datetime = datetime.now()
        past_datetime = current_datetime - timedelta(days=5)
        users = await session.scalars(select(User).where(
            and_(User.last_enter < past_datetime, User.last_notification < past_datetime)))
        return users


async def update_notification_info(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.last_notification = func.now()
        await session.commit()


async def set_user(tg_id: int, username: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            user = User(
                tg_id=tg_id,
                username=username
            )
            session.add(user)
            await session.commit()
        else:
            user.last_enter = func.now()
            await session.commit()


async def update_user_info(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.last_enter = func.now()
        await session.commit()


async def get_task_and_answer(task_type: str):
    async with async_session() as session:
        random_item = await session.scalars(
            select(Task).where(Task.type == task_type
                               ).order_by(func.random()).limit(1))
        return random_item.first()


async def get_json(tg_id: int):
    async with async_session() as session:
        user_task_info = await session.scalar(select(User.task_info).where(User.tg_id == tg_id))
        # print(type(user_task_info))
        js = ast.literal_eval(user_task_info)
        # print(type(js))
        return js


async def update_user_task_info(tg_id: int, js):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        js_str = str(js)
        user.task_info = js_str
        await session.commit()


async def get_task_and_answer_2(tg_id: int, task_type: str):
    async with async_session() as session:
        js = await get_json(tg_id)
        # print(type(js))
        # print(type(js[int(task_type)]))
        offset_num = int(js[int(task_type)])
        item = await session.scalars(
            select(Task).where(Task.type == task_type
                               ).offset(offset_num-1).limit(1))
        if js[int(task_type)] >= 30:
            js[int(task_type)] = 1
        else:
            js[int(task_type)] += 1
        await update_user_task_info(tg_id, js)
        return item.first()


async def get_random_task():
    async with async_session() as session:
        random_item = await session.scalars(
            select(Task).order_by(func.random()).limit(1))
        return random_item.first()


async def show_all_users():
    async with async_session() as session:
        all_users = await session.scalars(select(User))
        return all_users


async def delete_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        await session.delete(user)
        await session.commit()
