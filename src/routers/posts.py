from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dependencies import get_async_session
from src.database.models.posts import Post
from src.services.login import get_current_user

from src.services.posts import create_post, get_all_post, get_one_post, update_post, delete_post
from src.schemas.posts import PostCreate, PostUpdate
from src.schemas.posts import PostResponse

post_router = APIRouter(tags=['Post'])


@post_router.post('/', response_model=PostResponse, status_code=201)
async def create_post_api(data: PostCreate,
                          user=Depends(get_current_user),
                          session: AsyncSession = Depends(get_async_session)):
    return await create_post(data=data, session=session, user=user)


@post_router.get('/')
async def get_all_posts_api(session: AsyncSession = Depends(get_async_session)):
    return await get_all_post(session=session)


@post_router.get('/{pk}')
async def get_one_post_api(pk: int, session: AsyncSession = Depends(get_async_session)):
    return await get_one_post(pk=pk, session=session)


@post_router.put('/{pk}')
async def update_post_api(pk: int,
                          data: PostUpdate,
                          user=Depends(get_current_user),
                          session: AsyncSession = Depends(get_async_session)
                          ):
    return await update_post(pk=pk, data=data, session=session)


@post_router.delete('/{pk}', status_code=204)
async def delete_post_api(pk: int,
                          user=Depends(get_current_user),
                          session: AsyncSession = Depends(get_async_session)):
    await delete_post(pk=pk, session=session)
    return {'msg': 'Success'}

