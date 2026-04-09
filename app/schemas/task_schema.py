from pydantic import BaseModel
from app.enum_fdr.status_enum import Status
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: str
    # employee_email:str
    # assigned_by: str
    # assigned_to: str
    status: Status
    # mnc_id: Optional[int] = None
    # employee_id: int
    # organization_id: Optional[int] = None
    
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    assigned_by: str
    assigned_to: str
    status: Status
    mnc_id: Optional[int]
    employee_id: int
    organization_id: Optional[int]

    
    
    
class TaskUpdate(BaseModel):
    title:str
    description:str
    assigned_by:str
    assigned_to:str
    status:Status
    mnc_id:int
    employee_id:int
    organization_id:int


class TaskStatusUpdate(BaseModel):
    status:Status
    
    class Config:
        from_attributes = True