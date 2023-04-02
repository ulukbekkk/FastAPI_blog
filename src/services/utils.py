from src.config.settings import general

from datetime import datetime, timedelta
from typing import Dict, Union, Any, Optional
from jose import jwt
from passlib.context import CryptContext


class Hasher:
    pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str):
        res = self.pass_context.verify(plain_password, hashed_password)
        return res

    def get_password_hash(self, password: str):
        return self.pass_context.hash(password)


hasher = Hasher()


"""constants for creating access and refresh tokens"""

ACCESS_TOKEN_EXPIRE_MINUTES = general.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = general.refresh_token_expire_minutes
ALGORITHM = general.algorithm
JWT_ACCESS_SECRET_KEY = general.jwt_access_secret_key
JWT_REFRESH_SECRET_KEY = general.jwt_refresh_secret_key

"""functions for generating access and refresh tokens"""


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_refresh_token(token):
    decoded_jwt = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    user_phone = decoded_jwt.get("sub")
    exps = decoded_jwt.get('exp')
    return user_phone, exps


def decode_access_token(token):
    decoded_jwt = jwt.decode(token, JWT_ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
    user_phone = decoded_jwt.get("sub")
    exps = decoded_jwt.get('exp')
    return user_phone, exps


# security = HTTPBearer()


