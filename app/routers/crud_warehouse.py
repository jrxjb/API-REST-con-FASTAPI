from fastapi import APIRouter,HTTPException,Depends
from models.warehouse import  warehouseCreate
from datetime import datetime
from DataBase.DataBase import warehouse_collection, users_collection
from bson import ObjectId
from schemas.schemas_warehouse import warehouseEntity,warehouseEntityAll
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer   
import os 
from typing import Annotated
from jose import jwt
from schemas.user import userEntity


warehouse = APIRouter()

###################
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM =  os.getenv("ALGORITHM")
PEPPER = os.getenv("PEPPER")
ACCESS_TOKEN_EXPIRE_MINUTES = 2
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token:Annotated[str,Depends(OAuth2_scheme)])->dict:
    data = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    email = data.get("email")
    user = users_collection.find_one({"email": email})
    if user is None: 
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return userEntity(user)


def admin_required(current_user: dict = Depends(decode_token)):
    if current_user.get("is_admin") != True:
        raise HTTPException(status_code=403, detail="Denegated Access")
    return current_user

###################






@warehouse.post('/warehouse',tags=["warehouse"])
async def create_warehouse(warehouse:warehouseCreate,current_user: dict = Depends(admin_required)):
    try:
        new_warehouse = warehouse.dict()
        new_warehouse['created'] = datetime.utcnow().isoformat()
        new_warehouse['updated'] = datetime.utcnow().isoformat()
        admin_id=current_user.get("id")
        new_warehouse['adminAsigned'] = admin_id
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
async def put_one_warehouse(id:str,warehouse_D: warehouseCreate,current_user: dict = Depends(admin_required)):
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
async def delete_one_warehouse(id:str,current_user: dict = Depends(admin_required)):
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

