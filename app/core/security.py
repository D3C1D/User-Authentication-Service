import os

from dotenv import load_dotenv

from jose import jwt
from jose import JWTError

from datetime import (
    datetime,
    timedelta,
    timezone
)

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


oauth2_scheme = (
    OAuth2PasswordBearer(
        tokenUrl="login"
    )
)


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

        if not email:

            return None

        return email

    except JWTError:

        return None