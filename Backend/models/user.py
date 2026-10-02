from pydantic import BaseModel, Field


class user(BaseModel):
    name : str
    email : str
    password : str
    role : str = Field(default = "employee")