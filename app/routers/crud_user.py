from fastapi import APIRouter,Response,HTTPException
from models.user import userCreate,userOut,userDB
from DataBase.DataBase import users_collection
from datetime import datetime
from schemas.user import userEntity,usersEntity
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from passlib.hash import bcrypt
import os 
from dotenv import load_dotenv

#passlib  pip install passlib
user= APIRouter()
load_dotenv()

#find user
def find_user(id):
    return users_collection.find_one({'_id':ObjectId(id)})

PEPPER = os.getenv("PEPPER")

 
@user.post('/users',tags=["users"])
async def create_user(user:userCreate):
    try:
        new_user = user.dict()
        new_user["password"] = bcrypt.hash(new_user["password"]+ PEPPER)
        new_user['created'] = datetime.utcnow()
        new_user['updated'] = datetime.utcnow()
        new_user['active']  = True
        new_user['is_admin'] = False
        id = users_collection.insert_one(new_user).inserted_id
        user = users_collection.find_one({"_id":ObjectId(id)})
        return userEntity(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user.get('/get_users',response_model=list[userOut],tags=["users"])
async def find_all_user():
    return usersEntity(users_collection.find())


@user.get('/user/{id}',tags=["users"])
async def get_one_user(id:str):
    user = find_user(id)
    return userEntity(user)


@user.delete('/user{id}',tags=["users"])
async def delete_one_user_bool(id:str):
    user = find_user(id)
    user["active"] = False
    user['updated'] = datetime.utcnow()
    user = users_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return userEntity(user)


@user.put('/user/{id}',tags=["users"])
async def update_one_user(id:str,user:userCreate):
    user = user.dict()
    user['updated'] = datetime.utcnow()
    user = users_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return userEntity(user)


"""
@user.delete('/user{id}',tags=["users"])
async def delete_one_user(id:str):
    result = users_collection.delete_one({"_id":ObjectId(id)})
    if result.deleted_count ==  True :
     return Response(status_code=204)
    raise HTTPException(status_code=404,detail="Error")
"""

#uvicorn main:app --reload