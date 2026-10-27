from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name : str
    email : EmailStr
    password : str
    role : str = "employee"
    department_code: str
    employee_number: str
    individual_id: str | None = None

class UserLogin(BaseModel):
    email : str
    password : str


class UserUpdate(BaseModel):
    name : str| None = None
    email : EmailStr | None = None
    role : str | None = None

class ChangePassword(BaseModel):
    current_password : str 
    new_password : str   

class AdminChangePassword(BaseModel):
    new_password: str    