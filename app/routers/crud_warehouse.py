from fastapi import APIRouter,HTTPException
from models.warehouse import  warehouseCreate
from datetime import datetime
from DataBase.DataBase import warehouse_collection
from bson import ObjectId
from schemas.schemas_warehouse import warehouseEntity,warehouseEntityAll


warehouse = APIRouter()

@warehouse.post('/warehouse',tags=["warehouse"])
async def create_warehouse(warehouse:warehouseCreate):
    try:
        new_warehouse = warehouse.dict()
        new_warehouse['created'] = datetime.utcnow().isoformat()
        new_warehouse['updated'] = datetime.utcnow().isoformat()
        id   = warehouse_collection.insert_one(new_warehouse).inserted_id
        warehouse = warehouse_collection.find_one({"_id":ObjectId(id)})
        if not warehouse:
            raise HTTPException(status_code=404,detail="Warehouse not found")
        return warehouseEntity(warehouse)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    


@warehouse.get('/warehouse{id}',tags=["warehouse"])
async def get_one_warehouse(id:str):
    try:
        warehouse=warehouse_collection.find_one({"_id":ObjectId(id)})
        if (warehouse['active'] == False):
            return HTTPException(status_code=404, detail=str("Deleted"))
        if warehouse is None:
            return HTTPException(status_code=404, detail=str("Not Found"))
        return warehouseEntity(warehouse)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@warehouse.get('/warehouse',tags=["warehouse"])
async def get_warehouse():
    try:
        warehouse = warehouse_collection.find()
        if warehouse is None:
            return HTTPException(status_code=404, detail=str("Not Found"))
        return warehouseEntityAll(warehouse)
    except Exception as e:        
        raise HTTPException(status_code=500,detail=str(e))


@warehouse.put('/warehouse/{id}',tags=["warehouse"])
async def put_one_warehouse(id:str,warehouse_D: warehouseCreate):
    try:
        warehouse=warehouse_D.dict()
        warehouse['updated'] = datetime.utcnow().isoformat()
        warehouse = warehouse_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(warehouse)},return_document=True)
        if not warehouse:
            raise HTTPException(status_code=404,detail="Warehouse not found")   
        return warehouseEntity(warehouse)
    except Exception as e:  
        raise HTTPException(status_code=500,detail=str(e))

@warehouse.delete('/warehouse/{id}',tags=["warehouse"])
async def delete_one_warehouse(id:str):
    try:
        warehouse=warehouse_collection.find_one({"_id":ObjectId(id)})
        if not warehouse:
            raise HTTPException(status_code=404,detail="Warehouse not found")
        warehouse['active'] = False
        warehouse['updated'] = datetime.utcnow().isoformat()
        warehouse_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": warehouse})
        return warehouseEntity(warehouse)
    except Exception as e:  
        raise HTTPException(status_code=500,detail=str(e))

