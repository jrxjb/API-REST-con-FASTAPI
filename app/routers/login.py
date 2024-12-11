from fastapi import  Form,Depends,APIRouter,HTTPException
from typing import Annotated
from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
from DataBase.DataBase import users_collection
from schemas.user import userEntity
from jose import jwt
from passlib.hash import bcrypt
from.crud_user import PEPPER
import os 
from dotenv import load_dotenv



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

@appL.post('/token',tags=["users"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = users_collection.find_one({"email": form_data.username})
    if (not user)or ( not bcrypt.verify(form_data.password + PEPPER, user["password"])):
         raise HTTPException(status_code=400,detail="incorrect")
    token = encode_token({"username":user["name"], "email":user["email"]})
    return {"access_token":token}


@appL.get('/users/profile',tags=["users"])
async def profile(my_user:Annotated[dict, Depends(decode_token)]):
    return my_user