from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserCreate, UserLogin, UserUpdate, ChangePassword, AdminChangePassword
from services.user_service import (create_user, login_user as login_user_service, get_all_users, get_user_by_id, update_user, delete_user,change_password, admin_change_password)
from fastapi.security import HTTPAuthorizationCredentials
from utils.security import (get_current_user, security, require_admin, require_manager)
import os 
import shutil
from uuid import uuid4
from pathlib import Path
from fastapi import File, Form, UploadFile, HTTPException

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True,exist_ok=True)

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/")
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form("employee"),
    department_code: str = Form(...),
    employee_number: str = Form(...),
    profile_photo: UploadFile | None = File(None), 
):

    photo_path = None

    if profile_photo and profile_photo.filename:
        extension = Path(profile_photo.filename).suffix.lower()

        if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
            raise HTTPException(
                status_code=400,
                detail="Only JPG, PNG, and WEBP images are allowed"
            )

        filename = f"{uuid4().hex}{extension}"
        file_path = UPLOAD_DIR / filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(profile_photo.file, buffer)
            
        photo_path = f"uploads/{filename}"

    user = UserCreate(
        name=name,
        email=email,
        password=password,
        role=role,
        department_code=department_code,
        employee_number=employee_number
    )

    user_data = user.model_dump()
    user_data["profile_photo"] = photo_path


    return create_user(user_data)

@router.post("/login")
def login_user(user:UserLogin):
    return login_user_service(user)


@router.get("/me")
def get_my_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)

    user = get_user_by_id(current_user["user_id"])

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message" : "Profile retrieved successfully!",
        "user": user
    }


@router.put("/change-password")
def change_user_password(
    data: ChangePassword,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)
    try:
        result = change_password(
            str(current_user["user_id"]),
            data.current_password,
            data.new_password
        )

        if not result:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "message": "Password changed successfully!"
        }    

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.put("/{user_id}/password")
def admin_change_user_password(
    user_id:str,
    data:AdminChangePassword,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = get_current_user(credentials)

    require_admin(current_user)

    try:
        result = admin_change_password(
            user_id,
            data.new_password
        )
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail = "user not found"
            )

        return {
            "message": "user password changed successfully"
        }    

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )    

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