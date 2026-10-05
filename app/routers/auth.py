from fastapi import APIRouter
from app.schemas.user import RegisterRequest

router = APIRouter()

@router.post("/register")
def register(
    request: RegisterRequest
):
    return {
    "message":
        "register endpoint working"
}