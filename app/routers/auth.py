from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import (
    Session
)

from app.schemas.user import (
    RegisterRequest,
    LoginRequest
)

from app.database.session import (
    get_db
)

from app.models.user import (
    User
)

from app.services.hash_service import (
    hash_password,
    verify_password
)

from app.services.auth_service import (
    get_current_user
)

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token
)


router = APIRouter()


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_email = (
        db.query(User)
        .filter(
            User.email == request.email
        )
        .first()
    )

    if existing_email:

        return {
            "message":
                "Email already registered"
        }

    existing_username = (
        db.query(User)
        .filter(
            User.username == request.username
        )
        .first()
    )

    if existing_username:

        return {
            "message":
                "Username already exists"
        }

    hashed_pw = hash_password(
        request.password
    )

    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password=hashed_pw
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message":
            "User registered successfully"
    }


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.email == request.email
        )
        .first()
    )

    if not user:

        return {
            "message":
                "Invalid email or password"
        }

    is_valid = verify_password(
        request.password,
        user.hashed_password
    )

    if not is_valid:

        return {
            "message":
                "Invalid email or password"
        }

    access_token = (
        create_access_token(
            {
                "sub": user.email
            }
        )
    )

    refresh_token = (
        create_refresh_token(
            {
                "sub": user.email
            }
        )
    )

    return {
        "access_token":
            access_token,
        "refresh_token":
            refresh_token,
        "token_type":
            "bearer"
    }


@router.post("/refresh")
def refresh_token(
    token: str
):

    email = decode_refresh_token(
        token
    )

    if not email:

        return {
            "message":
                "Invalid refresh token"
        }

    access_token = (
        create_access_token(
            {
                "sub": email
            }
        )
    )

    return {
        "access_token":
            access_token,
        "token_type":
            "bearer"
    }


@router.get("/me")
def get_me(

    current_user: User = Depends(
        get_current_user
    )

):

    if not current_user:

        return {
            "message":
                "Not authenticated"
        }

    return {

        "id":
            current_user.id,

        "username":
            current_user.username,

        "email":
            current_user.email,

        "role":
            current_user.role,

        "is_active":
            current_user.is_active

    }