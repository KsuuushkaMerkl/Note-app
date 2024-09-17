from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from auth.models import User
from auth.schemas import UserRegisterRequestSchema
from auth.security import manager, pwd_context, limiter
from core.database import create_session
from notes.endpoints import router

app = FastAPI(
    title="Notes App"
)

app.include_router(router, prefix="/note", tags=["Notes"])


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@manager.user_loader()
def query_user(login: str):
    return create_session().query(User).filter(User.login == login).first()


@app.post("/register")
@limiter.limit("5/minute")
async def register(user: UserRegisterRequestSchema):
    db = create_session()
    existing_user = db.query(User).filter_by(login=user.login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User is already registered.")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(login=user.login, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.id


@app.post("/login")
@limiter.limit("5/minute")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = query_user(username)
    if not user:
        raise InvalidCredentialsException
    elif not pwd_context.verify(password, user.password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub": username})
    return {"access_token": access_token}

