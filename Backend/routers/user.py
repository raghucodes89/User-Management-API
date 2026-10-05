from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserCreate, UserLogin, UserUpdate
from services.user_service import (create_user, login_user as login_user_service, get_all_users, get_user_by_id, update_user, delete_user)
from fastapi.security import HTTPAuthorizationCredentials
from utils.security import (get_current_user, security, require_admin, require_manager)




router = APIRouter(prefix="/users", tags=["user"])


@router.post("/")
def register_user(user: UserCreate):
    return create_user(user)


@router.post("/login")
def login_user(user:UserLogin):
    return login_user_service(user)


@router.get("/me")
def get_my_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)

    return {
        "message" : "Authonticated successfully!",
        "user": current_user
    }

@router.get("/admin")
def admin_only(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)
    require_admin(current_user)

    return {
        "message" : "Welcome Admin",
        "user" : current_user
    }


@router.get("/manager")
def manager_only(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)
    require_manager(current_user)

    return {
        "message" : "Welcome Manager",
        "user" : current_user
    }


@router.get("/users")
def get_users(
    credentials : HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)
    require_manager(current_user)

    return get_all_users()

@router.get("/{user_id}")
def get_user(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)
    require_manager(current_user)

    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code =404,
            detail = "user not found"
        )
    return user    


@router.put("/{user_id}")
def update_user_details(
    user_id : str,
    data : UserUpdate,
    credentials : HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)
    require_manager(current_user)

    if data.role is not None and current_user.get("role") != "admin":
        raise HTTPException(
            status_code = 403,
            detail = "Only Admin Can Change User Role"
        )

    user = update_user(user_id, data)

    if not user:
        raise HTTPException(
            status_code = 404,detail = "User not found"
        )
    return user    

@router.delete("/{user_id}")
def delete_user_details(
    user_id : str,
    credentials : HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)
    require_admin(current_user)

    deleted = delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    return {
        "message" : "User deleted successfully"
    }

