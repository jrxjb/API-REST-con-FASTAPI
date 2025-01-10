from schemas.schemas_warehouse import warehouseEntity


def userEntity(item) -> dict:
    if item.get("warehouse"):
        warehouse_info = warehouseEntity(item["warehouse"])
    else:
        warehouse_info = None

    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "lastname": item["lastname"],
        "email": item["email"],
        "created": item["created"].isoformat(),
        "updated": item["updated"].isoformat(),
        "active": item["active"],
        "is_admin": item["is_admin"],
        "warehouse": warehouse_info
    }





"""def userEntity(item)-> dict:
    return{
        "id":str(item["_id"]),
        "name":item["name"],
        "lastname":item["lastname"],
        "email":item["email"],
        "created":item["created"].isoformat(),
        "updated":item["updated"].isoformat(),
        "active":item["active"],
        "is_admin":item["is_admin"],
        "warehouse": str(item["warehouse"]) if item.get("warehouse") else None
    }

"""


def usersEntity(entity) -> list:
    return[userEntity(item) for item in entity if item ["active"]]





#    "warehouse": str(item["warehouse"]) if item.get("warehouse") else None
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


