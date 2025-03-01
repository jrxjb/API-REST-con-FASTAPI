from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from models.user import userAdmin, userOut,userAdminUpdate
from DataBase.DataBase import users_collection
from schemas.user import userEntity,userAdminEntity,usersAdminEntity
from datetime import datetime
from bson import ObjectId
from passlib.hash import bcrypt
from jose import jwt
from .crud_user import PEPPER
import os
from dotenv import load_dotenv
from pymongo import ReturnDocument

admin= APIRouter()
load_dotenv()

#find user

appL= APIRouter()
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM =  os.getenv("ALGORITHM")
PEPPER = os.getenv("PEPPER")
ACCESS_TOKEN_EXPIRE_MINUTES = 2
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def find_user_by_email(email: str):
    return users_collection.find_one({"email": email})

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


def find_user(id):
    return users_collection.find_one({'_id':ObjectId(id)})

PEPPER = os.getenv("PEPPER")
admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")
 

#admin startup

@admin.on_event("startup")
async def startup_event():
    try:
        admin_user = users_collection.find_one({"email": admin_email})
        if not admin_user:
            new_user_admin = {
                "name": "Admin",
                "lastname": "Admin",
                "email": admin_email,
                "password": bcrypt.hash(admin_password + PEPPER),
                "is_admin": True,
                "created": datetime.utcnow(),
                "updated": datetime.utcnow(),
                "active": True
            }
            id = users_collection.insert_one(new_user_admin).inserted_id
            user = users_collection.find_one({"_id": ObjectId(id)})
            print("Usuario administrador creado con éxito")
            return userEntity(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#admin Create (POST)

def admin_required(current_user: dict = Depends(decode_token),tags=["admin"]):
    if current_user.get("is_admin") != True:
        raise HTTPException(status_code=403, detail="Denegated Access")
    return current_user

@admin.post('/create_admin',tags=["admin"])
async def create_admin (user:userAdmin, current_user:dict = Depends(admin_required)):
    try:
        new_user = user.dict()
        if users_collection.find_one({"email":new_user["email"]}): 
         raise HTTPException(status_code=400, detail="Email already exists")
        new_user["password"] = bcrypt.hash(new_user["password"]+ PEPPER)
        new_user['created'] = datetime.utcnow()
        new_user['updated'] = datetime.utcnow()
        new_user['active']  = True
        new_user['is_admin'] = True
        id = users_collection.insert_one(new_user).inserted_id
        user = users_collection.find_one({"_id": ObjectId(id)})
        return userEntity(user)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

 
@admin.get('/get_admins',response_model=list[userOut],tags=["admin"])
async def find_all_admin(current_user:dict = Depends(admin_required)):
    admin= users_collection.find({"is_admin":True})
    return usersAdminEntity(admin)


def updated(id: str, newAdmin2: dict):
    user = users_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": newAdmin2},
        return_document=ReturnDocument.AFTER
    )
    return user


@admin.put('/user/{id}', tags=["admin"])
async def update_one_admin(id: str, newAdmin: userAdminUpdate, current_user: dict = Depends(admin_required)):
    try:
        newAdmin2 = newAdmin.dict(exclude_unset=True)
        newAdmin2['updated'] = datetime.utcnow()
        user = updated(id, newAdmin2)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return userAdminEntity(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@admin.delete('/delete_admin{id}',tags=["admin"])
async def delete_admin(id:str,current_user:dict = Depends(admin_required)):
    user = find_user(id)
    if user["is_admin"] != False:
        raise HTTPException(status_code=403, detail="inactive admin")
    user["active"] = False
    user['updated'] = datetime.utcnow()
    user = users_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return userEntity(user)
