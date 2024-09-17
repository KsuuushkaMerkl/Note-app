from fastapi_login import LoginManager

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = "a930483a9f6058258b8a618091d87030217358c93fe10253"
manager = LoginManager(SECRET, "/login")