from fastapi import (
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import (
    Session
)

from app.database.session import (
    get_db
)

from app.core.security import (
    oauth2_scheme,
    decode_access_token
)

from app.models.user import (
    User
)


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

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


def get_current_admin(

    current_user: User = Depends(
        get_current_user
    )

):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user