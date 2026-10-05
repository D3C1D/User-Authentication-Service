import bcrypt
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import (
oauth2_scheme,
decode_access_token
)
from app.models.user import User

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(
        password_bytes,
        salt
    )
    return hashed_password.decode("utf-8")

def get_current_user(
    token: str = Depends(
        oauth2_scheme
    ),
    db: Session = Depends(
        get_db
    )
):
    email = decode_access_token(
        token
    )
    if not email:
        return None
    user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )
    return user