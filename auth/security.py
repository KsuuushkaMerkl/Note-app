from fastapi_login import LoginManager

from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import get_remote_address

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = "a930483a9f6058258b8a618091d87030217358c93fe10253"
manager = LoginManager(SECRET, "/login")

limiter = Limiter(key_func=get_remote_address)