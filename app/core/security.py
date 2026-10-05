from jose import jwt
from datetime import (
    datetime,
    timedelta,
    timezone
)
from jose import JWTError
from fastapi.security import (
    OAuth2PasswordBearer
)

SECRET_KEY = (
    "super-secret-key-change-later"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(
        data: dict
):
    to_encode = data.copy()
    expire = (
        datetime.now(timezone.utc)
        +
        timedelta(
            minutes=
            ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )
    to_encode.update(
        {
            "exp": expire
        }
    )
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

def decode_access_token(
    token: str
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM
            ]
        )
        email = payload.get(
            "sub"
        )
        return email
    except JWTError:
        return None

oauth2_scheme = (
    OAuth2PasswordBearer(
        tokenUrl="login"
    )
)