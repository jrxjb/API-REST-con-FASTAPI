from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class ItemsCreate(BaseModel):
    brand: str
    model: str
    features: Optional[List[str]] = Field(default_factory=list)
    warehouse: str 

    model_config = ConfigDict(arbitrary_types_allowed=True)


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
    warehouse: Optional[dict] = None



class ItemsUser(BaseModel):
    brand: str
    model: str
    sold_date:Optional[datetime] = None
    out_of_stock: bool
    features: Optional[List[str]] = []

