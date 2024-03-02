from __future__ import annotations

import asyncio
import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import selectinload


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Property(Base):
    __tablename__ = "property"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    create_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())


# async def insert_objects(async_session: async_sessionmaker[AsyncSession]) -> None:
#     async with async_session() as session:
#         async with session.begin():
#             session.add_all(
#                 [
#                     A(bs=[B(data="b1"), B(data="b2")], data="a1"),
#                     A(bs=[], data="a2"),
#                     A(bs=[B(data="b3"), B(data="b4")], data="a3"),
#                 ]
#             )


# async def select_and_update_objects(
#     async_session: async_sessionmaker[AsyncSession],
# ) -> None:
#     async with async_session() as session:
#         stmt = select(A).options(selectinload(A.bs))
#
#         result = await session.execute(stmt)
#
#         for a in result.scalars():
#             print(a)
#             print(f"created at: {a.create_date}")
#             for b in a.bs:
#                 print(b, b.data)
#
#         result = await session.execute(select(A).order_by(A.id).limit(1))
#
#         a1 = result.scalars().one()
#
#         a1.data = "new data"
#
#         await session.commit()
#
#         # access attribute subsequent to commit; this is what
#         # expire_on_commit=False allows
#         print(a1.data)
#
#         # alternatively, AsyncAttrs may be used to access any attribute
#         # as an awaitable (new in 2.0.13)
#         for b1 in await a1.awaitable_attrs.bs:
#             print(b1, b1.data)

engine = create_async_engine(
    "postgresql+asyncpg://engineer:pecia9911sol!@localhost:5432/public",
    echo=True,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    await session.commit()
    await engine.dispose()
