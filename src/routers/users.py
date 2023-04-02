from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer


from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dependencies import get_async_session
from src.database.models.users import User
from src.services.users import (create_user, get_all_user, delete_user)
from src.services.login import (user_login, refresh_token_change, get_current_user)
from src.schemas.users import (UserCreateSchema, UserResponseSchema)
from src.schemas.tokens import TokenResponse, TokenBaseResponse

user_router = APIRouter(tags=['User'])


@user_router.post('/registration', response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user_api(data: UserCreateSchema,
                          session: AsyncSession = Depends(get_async_session)):
    user: User = await create_user(data=data, session=session)
    return user


@user_router.get('/all', )
async def get_all_user_api(session: AsyncSession = Depends(get_async_session)):
    return await get_all_user(session=session)


@user_router.post('/login', response_model=TokenResponse, status_code=status.HTTP_200_OK,)
async def user_login_api(data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    return await user_login(data=data, session=session)


@user_router.post('/refresh', response_model=TokenBaseResponse, status_code=status.HTTP_200_OK)
async def change_access_token_api(refresh_token: str, ):
    return await refresh_token_change(refresh_token=refresh_token)


@user_router.delete('/user_me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_profile_api(user: User = Depends(get_current_user),
                                  session: AsyncSession = Depends(get_async_session)):
    await delete_user(user=user, session=session)
    return {'msg': 'Success'}
