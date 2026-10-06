import os
import secrets

from datetime import (
    datetime,
    timedelta,
    timezone
)

from dotenv import load_dotenv

from jose import JWTError
from jose import jwt

from fastapi.security import (
    OAuth2PasswordBearer
)

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY not found"
    )

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        30
    )
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE_DAYS",
        7
    )
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def create_access_token(
    data: dict
) -> str:

    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "access"
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(
    data: dict
) -> str:

    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "refresh"
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

        token_type = payload.get(
            "type"
        )

        if token_type != "access":
            return None

        email = payload.get(
            "sub"
        )

        if not email:
            return None

        return email

    except JWTError:

        return None


def decode_refresh_token(
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

        token_type = payload.get(
            "type"
        )

        if token_type != "refresh":
            return None

        email = payload.get(
            "sub"
        )

        if not email:
            return None

        return email

    except JWTError:

        return None


def verify_token(
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

        return payload

    except JWTError:

        return None

def create_password_reset_token():

    return secrets.token_urlsafe(
        32
    )