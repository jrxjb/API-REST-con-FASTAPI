from fastapi import APIRouter,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from models.user import userCreate,userOut,userUpdate
from DataBase.DataBase import users_collection, warehouse_collection
from datetime import datetime
from schemas.user import userEntity,usersEntity
from bson import ObjectId
from passlib.hash import bcrypt
import os 
from dotenv import load_dotenv
from jose import jwt
from typing import Annotated,List

#passlib  pip install passlib
user= APIRouter()


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM =  os.getenv("ALGORITHM")
PEPPER = os.getenv("PEPPER")
ACCESS_TOKEN_EXPIRE_MINUTES = 2
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

###########

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



#find user
def find_user(id):
    return users_collection.find_one({'_id':ObjectId(id)})

PEPPER = os.getenv("PEPPER")

 
@user.post('/users',tags=["users"])
async def create_user(user:userCreate):
    try:

        new_user = user.dict()
        if users_collection.find_one({"email":new_user["email"]}): 
            raise HTTPException(status_code=400, detail="Email already exists")
        new_user["password"] = bcrypt.hash(new_user["password"]+ PEPPER)
        new_user['created'] = datetime.utcnow()
        new_user['updated'] = datetime.utcnow()
        new_user['active']  = True
        new_user['is_admin'] = False
        warehouse_id = new_user["warehouse"] 
        if len(warehouse_id) != 24: 
            raise HTTPException(status_code=404, detail="Warehouse id invalid")
        warehouse = warehouse_collection.find_one({"_id": ObjectId(new_user["warehouse"])})
        if not warehouse :
            raise HTTPException(status_code=404, detail="Warehouse not found")
        if not warehouse["active"]:
            raise HTTPException(status_code=404, detail="Warehouse not active")
        new_user["warehouse"] = warehouse
        id = users_collection.insert_one(new_user).inserted_id
        user = users_collection.find_one({"_id":ObjectId(id)})
        return userEntity(user)
    except HTTPException as http_exc: 
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

 
@user.get('/get_users', response_model=List[userOut], tags=["users"])
async def find_all_user(current_user: dict = Depends(decode_token)):
    try:
        if current_user["is_admin"]:
            return usersEntity(users_collection.find())
        else:
            id_user = current_user["id"]
            user = get_one_user(id_user)
            return user
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
    
    
@user.get('/user/{id}',tags=["users"])
async def get_one_user(id:str,current_user: dict = Depends(decode_token)):
    try:
        if current_user["id"] != id and not current_user["is_admin"]:
            raise HTTPException(status_code=403,detail="You are not authorized")
        user = find_user(id)
        if not user:
            raise HTTPException(status_code=404,detail="User not found")
        return userEntity(user)
    except HTTPException as http_exc: 
        raise http_exc
    except Exception as e:  
        raise HTTPException(status_code=404,detail="User not found")


@user.put('/user/{id}',tags=["users"])
async def update_one_user(id:str,user:userUpdate,current_user: dict = Depends(decode_token)):
    if current_user["id"] != id and not current_user["is_admin"]:
        raise HTTPException(status_code=403,detail="You are not authorized")
    user = user.dict()
    user['updated'] = datetime.utcnow()
    user = users_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return userEntity(user)


@user.delete('/user{id}',tags=["users"])
async def delete_one_user_bool(id:str,current_user: dict = Depends(admin_required)):
    user = find_user(id)
    user["active"] = False
    user['updated'] = datetime.utcnow()
    user = users_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return userEntity(user)




#uvicorn main:app --reload