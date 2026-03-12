from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BotonBase(BaseModel):
    nombre: str
    color: str

class BotonResponse(BotonBase):
    id: str  
    estado: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True
    
class BotonUpdate(BaseModel):
    nombre: Optional[str] = None
    color: Optional[str] = None
    estado: Optional[str] = None

