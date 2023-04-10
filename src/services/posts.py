from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from src.schemas.posts import PostCreate
from src.database.models.posts import Post


async def create_post(data: PostCreate, user, session: AsyncSession):
    post = Post(**data.dict(), user=user)
    session.add(post)
    await session.commit()
    return post


async def get_all_post(session: AsyncSession):
    posts_query: list[Post] = (await session.scalars(select(Post))).all()
    return posts_query


async def get_one_post(pk, session: AsyncSession):
    post_query: Post = await session.scalar(select(Post).where(Post.id == pk))
    return post_query


async def update_post(pk, data, session: AsyncSession):
    post_query = await session.execute(
        update(Post)
        .where(Post.id == pk)
        .values(**data.dict())
    )
    await session.commit()


async def delete_post(pk, session: AsyncSession):
    await session.execute(delete(Post).where(Post.id == pk))
    await session.commit()
