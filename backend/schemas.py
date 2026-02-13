from pydantic import BaseModel


class RegisterBody(BaseModel):
    username: str
    password: str
    turnstile_token: str


class LoginBody(BaseModel):
    username: str
    password: str
    turnstile_token: str
