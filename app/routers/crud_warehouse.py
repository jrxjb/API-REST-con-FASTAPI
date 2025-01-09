from fastapi import APIRouter,HTTPException
from models.warehouse import  warehouseCreate,warehouseDB
from datetime import datetime
from DataBase.DataBase import warehouse_collection
from bson import ObjectId
from schemas.schemas_warehouse import warehouseEntity,warehouseEntityAll
from typing import Union,List

warehouse = APIRouter()

@warehouse.post('/warehouse',tags=["warehouse"])
async def create_warehouse(warehouse:warehouseCreate):
    new_warehouse = warehouse.dict()
    new_warehouse['created'] = datetime.utcnow().isoformat()
    new_warehouse['updated'] = datetime.utcnow().isoformat()
    id   = warehouse_collection.insert_one(new_warehouse).inserted_id
    warehouse = warehouse_collection.find_one({"_id":ObjectId(id)})
    return warehouseEntity(warehouse)


@warehouse.get('/warehouse{id}',tags=["warehouse"])
async def get_one_warehouse(id:str):
    warehouse=warehouse_collection.find_one({"_id":ObjectId(id)})
    if (warehouse['active'] == False):
        return HTTPException(status_code=404, detail=str("Deleted"))
    if warehouse is None:
        return HTTPException(status_code=404, detail=str("Not Found"))
    return warehouseEntity(warehouse)

@warehouse.get('/warehouse',tags=["warehouse"])
async def get_warehouse():
    warehouse = warehouse_collection.find()
    if warehouse is None:
        return HTTPException(status_code=404, detail=str("Not Found"))
    return warehouseEntityAll(warehouse)

