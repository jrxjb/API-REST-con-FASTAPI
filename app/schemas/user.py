from typing import List,Any,Dict

def userEntity(item)-> dict:
    return{
        "id":str(item["_id"]),
        "name":item["name"],
        "lastname":item["lastname"],
        "email":item["email"],
        "created":item["created"].isoformat(),
        "updated":item["updated"].isoformat(),
        "active":item["active"],
        "is_admin":item["is_admin"]
    }

def usersEntity(entity
) -> list:
    return[userEntity(item) for item in entity]



def userEntityUpdate(item) -> list:
    return{
        "id":str(item["_id"]),
        "name":item["name"],
        "lastname":item["lastname"],
        "email":item["email"],
        "password":item["password"],
        "active":item["active"],
        "is_admin":item["is_admin"]
    }