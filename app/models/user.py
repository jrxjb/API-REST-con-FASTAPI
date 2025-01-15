from pydantic import BaseModel, Field
from typing import Optional
from models.warehouse import warehouseDB

class userCreate(BaseModel):
    name: str
    lastname:str
    email: str
    password: str
    warehouse: str


class userUpdate(BaseModel):

    name: str
    lastname:str
    email: str
    warehouse: str

class userUpdateByAdmin(BaseModel):

    name: str
    lastname:str
    email: str
    active: bool
    is_admin: bool
    warehouse: str


class userOut(BaseModel):
    id:str
    name: str
    lastname:str
    email: str
    created:str
    updated:str
    active: bool
    is_admin: bool
    warehouse: Optional[warehouseDB] = Field(None, description="")


class userAdmin(BaseModel):
    name: str
    lastname:str
    email: str
    password: str
    is_admin: bool
  

 #  warehouse: Optional[warehouseDB] = Field(None) 