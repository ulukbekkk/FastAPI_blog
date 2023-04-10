from pydantic import BaseModel
from src.schemas.users import UserResponseSchema


class BasePost(BaseModel):
    title: str
    text: str

    # user_id: int

    class Config:
        orm_mode = True


class PostCreate(BasePost):
    pass


class PostUpdate(BasePost):
    pass


class PostResponse(BasePost):
    id: int
    user: UserResponseSchema
