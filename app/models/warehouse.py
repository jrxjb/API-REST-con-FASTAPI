from pydantic import BaseModel

class warehouseCreate(BaseModel):
    name: str
    address:str
    active: bool


class warehouseDB(BaseModel):
    id:str
    name: str
    address:str
    created:str
    updated:str
    active: bool
    adminAsigned: str


