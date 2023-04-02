from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreateSchema(BaseUser):
    password: str


class UserResponseSchema(BaseUser):
    id: int
