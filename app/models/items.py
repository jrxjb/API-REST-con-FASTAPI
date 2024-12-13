from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime 

class ItemsCreate(BaseModel):
    brand: str
    model: str
    features: Optional[List[str]] = []


class ItemsInDB(BaseModel):
    id:str
    brand: str
    model: str
    sold_date:Optional[datetime] = None
    out_of_stock: bool
    created:str
    updated:str
    deleted:bool
    features: Optional[List[str]] = []



class ItemsUser(BaseModel):
    brand: str
    model: str
    sold_date:Optional[datetime] = None
    out_of_stock: bool
    features: Optional[List[str]] = []

