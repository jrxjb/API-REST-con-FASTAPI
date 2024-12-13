from fastapi import APIRouter,HTTPException
from models.items import ItemsCreate,ItemsInDB,ItemsUser
from datetime import datetime
from DataBase.DataBase import item_collection
from bson import ObjectId
from schemas.schemas_items import itemAdminEntity,itemUserEntity,itemADminEntityAll
from typing import Union,List


items = APIRouter()

@items.post('/items')
async def create_Item(item:ItemsCreate):
    new_item = item.dict()
    new_item['created'] = datetime.utcnow().isoformat()
    new_item['updated'] = datetime.utcnow().isoformat()
    new_item['deleted'] = False
    new_item['sold_date'] = None
    new_item['out_of_stock'] = False
    id   = item_collection.insert_one(new_item).inserted_id
    item = item_collection.find_one({"_id":ObjectId(id)})
    return itemAdminEntity(item)

#@items.get('/items',response_model=List[Union[List[ItemsInDB],List[ItemsUser]]])

@items.get('/items',response_model=List[ItemsInDB])
async def get_items():
    item = item_collection.find()
    return itemADminEntityAll(item)

@items.get('/items/{id}')
async def get_one_item(id:str):
    item=item_collection.find_one({"_id":ObjectId(id)})
    if (item['deleted'] == True):
        return HTTPException(status_code=404, detail=str("Deleted"))
    return itemAdminEntity(item)

@items.put('/items/{id}')
async def put_one_item(id:str,item:ItemsUser):
    item=item.dict()
    item['updated'] = datetime.utcnow().isoformat()
    item = item_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(item)},return_document=True)
    return itemAdminEntity(item)
    

@items.delete('/items/{id}')
def delete_one_item(id:str):
    item=item_collection.find_one({"_id":ObjectId(id)})
    item['deleted'] = True
    item['updated'] = datetime.utcnow().isoformat()
    item_collection.update_one({"_id": ObjectId(id)}, {"$set": item})
    return itemAdminEntity(item)