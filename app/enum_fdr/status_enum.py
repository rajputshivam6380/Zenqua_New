from enum import Enum
from pydantic import BaseModel

class Status(str,Enum):
    pending="pending"
    completed="completed"
    in_progress="in_progress"
    
