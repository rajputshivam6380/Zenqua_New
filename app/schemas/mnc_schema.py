from pydantic import BaseModel

class MncCreate(BaseModel):
    name:str
    created_by:str
    
    
class MncResponse(BaseModel):
    name:str
    created_by:str
    id:int
    
    
class MncUpdate(BaseModel):
    name:str
    created_by:str
    
    class Config:
        orm_mode = True
    
    