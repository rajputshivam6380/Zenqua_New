from pydantic import BaseModel

class OrgCreate(BaseModel):
    name:str
    # created_by:str
    mnc_id:int
    
    
class OrgResponse(BaseModel):
    name:str
    # created_by:str
    id:int
    mnc_id:int

    
class OrgUpdate(BaseModel):
    name: str
    mnc_id: int
    
    class Config:
        orm_mode = True
    
    