from fastapi import APIRouter
from schemas.user import UserCreate
from services.user_service import create_user



router = APIRouter(prefix="/users", tags=["user"])


@router.post("/")
def register_user(user: UserCreate):
    return create_user(user)