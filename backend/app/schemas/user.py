from pydantic import BaseModel,EmailStr, ConfigDict
from enum import Enum


class UserRole(str,Enum):
    ADMIN = "admin"
    DRIVER = "driver"
    USER = "user"
    

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    role: UserRole = UserRole.USER
    
class UserResponse(BaseModel):
    user_id:str
    email:EmailStr
    is_active:bool
    role:UserRole
    
    model_config =ConfigDict(from_attributes=True)
    
    