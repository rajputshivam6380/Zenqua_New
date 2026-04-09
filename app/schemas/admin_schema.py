from pydantic import BaseModel
from typing import Optional

class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str
    mnc_id: Optional[int] = None
    organization_id: Optional[int] = None