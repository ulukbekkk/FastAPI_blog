from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from fastapi import HTTPException, status

from src.schemas.users import UserCreateSchema
from src.database.models.users import User
from src.services.utils import hasher


async def create_user(session: AsyncSession, data: UserCreateSchema, ):
    user_query = await session.scalar(select(User).where(User.username == data.username))
    if user_query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'msg': 'Username already exist'})
    data.password = hasher.get_password_hash(data.password)
    user = User(**data.dict())
    session.add(user)
    await session.commit()
    return user


async def get_all_user(session: AsyncSession):
    user_query: User = (await session.scalars(select(User))).all()
    return user_query


async def delete_user(user: User, session: AsyncSession):
    await session.execute(delete(User).where(User.id == user.id))
    await session.commit()
