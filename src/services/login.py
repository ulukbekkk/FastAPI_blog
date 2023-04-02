from fastapi import HTTPException, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models.users import User
from src.services.utils import (hasher, create_access_token, create_refresh_token, decode_refresh_token,
                                decode_access_token)
from src.config.settings import general
from src.database.dependencies import get_async_session

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer

from datetime import timedelta, datetime

from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


async def user_login(data, session: AsyncSession):
    user: User = await session.scalar(select(User).where(User.username == data.username))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': 'User have not in server'})
    if not hasher.verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'msg': 'Wrong password'})
    access_token_expires = timedelta(minutes=general.access_token_expire_minutes)
    refresh_token_expires = timedelta(minutes=general.refresh_token_expire_minutes)

    tokens = {"access_token": create_access_token(data={'sub': user.username}, expires_delta=access_token_expires),
              "refresh_token": create_refresh_token(data={'sub': user.username}, expires_delta=refresh_token_expires),
              'token_type': 'bearer'}

    return tokens


async def refresh_token_change(refresh_token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        username, exps = decode_refresh_token(refresh_token)
        if not username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'msg': 'Wrong token'})

        if exps is None:
            raise credentials_exception

        if datetime.utcnow() > datetime.fromtimestamp(exps):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={'msg': 'Life of refresh token is finished'})

        access_token_expires = timedelta(minutes=general.access_token_expire_minutes)
        refresh_token_expires = timedelta(minutes=general.refresh_token_expire_minutes)
        token = {'access_token': create_access_token(data={'sub': username}, expires_delta=access_token_expires),
                 'refresh_token': create_refresh_token(data={'sub': username}, expires_delta=refresh_token_expires),
                 'token_type': 'bearer'}
        return token
    except JWTError:
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        username, exps = decode_access_token(token=token)

        if username is None:
            raise credentials_exception
        if exps is None:
            raise credentials_exception
        if datetime.utcnow() > datetime.fromtimestamp(exps):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={'msg': 'Life of refresh token is finished'})

    except JWTError:
        raise credentials_exception

    user = await session.scalar(select(User).where(User.username == username))
    if user is None:
        raise credentials_exception
    return user
