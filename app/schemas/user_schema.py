from pydantic import BaseModel
from typing import Optional
class UserCreate(BaseModel):
    name: str
    email: str
    password:str
    role:str
    mnc_id:Optional[int]=None
    organization_id:Optional[int]=None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    # password:str
    mnc_id:Optional[int]
    organization_id:Optional[int]


class UserUpdate(BaseModel):
    name: str
    email: str
    mnc_id:int
    organization_id:int
    password:str


class LoginSchema(BaseModel):
    email: str
    password: str
    
    
    
    
class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    mnc_id: Optional[int] = None
    organization_id: Optional[int] = None


    class Config:
         from_attributes = True
        
