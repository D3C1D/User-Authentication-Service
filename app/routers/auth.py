from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.user import (
RegisterRequest,
LoginRequest
)
from app.database.session import get_db
from app.models.user import User
from app.services.hash_service import (
    hash_password,
    verify_password
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
    return {
        "message":
            "Login successful"
    }