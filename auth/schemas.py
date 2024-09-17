from pydantic import BaseModel


class UserRegisterRequestSchema(BaseModel):
    login: str
    password: str
