import sqlalchemy
from sqlalchemy import BigInteger, String, ForeignKey, TIMESTAMP, DateTime
from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///db_history.sqlite3', pool_pre_ping=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(150), default='У пользователя нет никнейма')
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    last_enter: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    last_notification: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    task_info: Mapped[str] = mapped_column(default='{1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1,11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1}')


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(Text)
    task: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(String(150))
    answer: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(Text)
    row_num: Mapped[int] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
