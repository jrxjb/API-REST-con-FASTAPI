from fastapi import APIRouter,HTTPException,Depends,Body
from models.items import ItemsCreate,ItemsInDB,ItemsUser
from datetime import datetime
from DataBase.DataBase import item_collection,users_collection,warehouse_collection
from bson import ObjectId
from schemas.schemas_items import itemAdminEntity,itemADminEntityAll
from schemas.user import userEntity
from typing import Union,List
####
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
from typing import Annotated
from jose import jwt 



items = APIRouter()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM =  os.getenv("ALGORITHM")
PEPPER = os.getenv("PEPPER")
ACCESS_TOKEN_EXPIRE_MINUTES = 2
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def encode_token(payload:dict)->str:
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def decode_token(token:Annotated[str,Depends(OAuth2_scheme)])->dict:
    data = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    email = data.get("email")
    user = users_collection.find_one({"email": email})
    if user is None: 
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return userEntity(user)


def admin_required(current_user: dict = Depends(decode_token),tags=["admin"]):
    if current_user.get("is_admin") != True:
        raise HTTPException(status_code=403, detail="Denegated Access")
    return current_user

##################################
#POST
 
@items.post('/items')
async def create_Item(item:ItemsCreate ,currente_user:dict = Depends(admin_required)):
    try:
        new_item = item.dict()
        new_item['created'] = datetime.utcnow().isoformat()
        new_item['updated'] = datetime.utcnow().isoformat()
        new_item['deleted'] = False
        new_item['sold_date'] = None
        new_item['out_of_stock'] = False
        new_item['warehouseid'] = ObjectId(item.warehouse)
        if not item.warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        id   = item_collection.insert_one(new_item).inserted_id
        item = item_collection.find_one({"_id":ObjectId(id)})
        item['_id'] = str(item['_id']) 
        item['warehouseid'] = str(item['warehouseid'])
        return  itemAdminEntity(item)
    except HTTPException as http_exc: 
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
########################################################
#GET

@items.get('/items',response_model=List[ItemsInDB])
async def get_items(currente_user:dict = Depends(decode_token)):
    try:
        item = item_collection.find()
        items = list(item)
        return itemADminEntityAll(items)
    except Exception as e:  
        raise HTTPException(status_code=404,detail=str(e))


@items.get('/items/{id}')
async def get_one_item(id:str,currente_user:dict = Depends(decode_token)):
    try:
        item=item_collection.find_one({"_id":ObjectId(id)})
        if (item['deleted'] == True):
            return HTTPException(status_code=404, detail=str("Deleted"))
        return itemAdminEntity(item)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


##############################################################
#PUT

@items.put('/items/{id}')
async def put_one_item(id:str,item:ItemsUser,currente_user:dict = Depends(admin_required)):
    try:
        item_query = item_collection.find_one({"_id":ObjectId(id)})
        if not item_query:
            raise HTTPException(status_code=404,detail="Item not found")
        if (item_query['deleted']==True):
            raise HTTPException(status_code=404,detail="deleted")
        updated_data=item.dict()
        updated_data['updated'] = datetime.utcnow().isoformat()
        updated_data = item_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(item)},return_document=True)
        return itemAdminEntity(item)
    except HTTPException as http_exc: 
        raise http_exc
    except Exception as e:  
        raise HTTPException(status_code=404,detail=str(e))
    
##############################################################
#DELETE
@items.delete('/items/{id}')
def delete_one_item(id:str,currente_user:dict = Depends(admin_required)):
    try:
        item=item_collection.find_one({"_id":ObjectId(id)})
        if not item:
            raise HTTPException(status_code=404,detail="Item not found")
        if (item['deleted']==True):
            raise HTTPException(status_code=404,detail="Item already deleted")
        item['deleted'] = True
        item['updated'] = datetime.utcnow().isoformat()
        item_collection.update_one({"_id": ObjectId(id)}, {"$set": item})
        return {"message": "Item deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

