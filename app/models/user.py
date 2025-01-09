from pydantic import BaseModel
from typing import Optional

class userCreate(BaseModel):
    name: str
    lastname:str
    email: str
    password: str

    
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


class userAdmin(BaseModel):
    name: str
    lastname:str
    email: str
    password: str
    is_admin: bool