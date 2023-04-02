from pydantic import BaseModel


class TokenBaseResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenResponse(TokenBaseResponse):
    refresh_token: str


class TokenAccessResponse(TokenBaseResponse):
    pass
