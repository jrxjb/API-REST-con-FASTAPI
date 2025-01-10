from pydantic import BaseModel, Field
from typing import Optional
from models.warehouse import warehouseDB

class userCreate(BaseModel):
    name: str
    lastname:str
    email: str
    password: str
    warehouse: str


class userDB(BaseModel):
    id:str
    name: str
    lastname:str
    email: str
    passoword:str
    created:str
    updated:str
    active: bool
    is_admin: bool

class userOut(BaseModel):
    id:str
    name: str
    lastname:str
    email: str
    created:str
    updated:str
    active: bool
    is_admin: bool
    warehouse: Optional[warehouseDB] = Field(None, description="Información de la bodega asociada")


class userAdmin(BaseModel):
    name: str
    lastname:str
    email: str
    password: str
    is_admin: bool