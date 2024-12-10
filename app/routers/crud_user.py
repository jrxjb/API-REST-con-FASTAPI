from fastapi import APIRouter
from models.user import userCreate,userOut
from DataBase.DataBase import users_collection
from datetime import datetime
from schemas.user import userEntity,usersEntity
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

user= APIRouter()


#find user
def find_user(id):
    return users_collection.find_one({'_id':ObjectId(id)})

@user.post('/users',tags=["users"])
async def create_user(user:userCreate):
    new_user = user.dict()
    new_user['created'] = datetime.utcnow()
    new_user['updated'] = datetime.utcnow()
    new_user['active']  = True
    id = users_collection.insert_one(new_user).inserted_id
    user = users_collection.find_one({"_id":ObjectId(id)})
    return userEntity(user)

@user.get('/get_users',response_model=list[userOut],tags=["users"])
async def find_all_user():
    return usersEntity(users_collection.find())


@user.get('/user/{id}',tags=["users"])
async def get_one_user(id:str):
    user = find_user(id)
    return userEntity(user)



