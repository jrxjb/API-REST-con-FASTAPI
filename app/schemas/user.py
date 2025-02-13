from schemas.schemas_warehouse import warehouseEntity
from DataBase.DataBase import warehouse_collection
from bson import ObjectId

def userEntity(item) -> dict:
    warehouse_info = []
    if item.get("warehouse") and isinstance(item["warehouse"], dict):
        warehouse_info = [{
            "id": str(item["warehouse"].get("_id")),
            "name": item["warehouse"].get("name", ""),
            "address": item["warehouse"].get("address", ""),
            "created": item["warehouse"].get("created", ""),
            "updated": item["warehouse"].get("updated", ""),
            "active": item["warehouse"].get("active", False),
            "adminAsigned": str(item["warehouse"].get("adminAsigned", ""))
        }]
    
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

 


def usersEntity(entity) -> list:
    return[userEntity(item) for item in entity if item ["active"]]

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

def get_warehouses_for_user(user_warehouse: str) -> list:
    try:
        warehouse = warehouse_collection.find({"_id": ObjectId(user_warehouse)})
    except Exception as e:
        return []
    return [warehouseEntity(item) for item in warehouse]

def get_warehouse(admin_warehouse: str) -> list:
    warehouses = warehouse_collection.find({"adminAsigned": ObjectId(admin_warehouse)})
    return [{
            "id": str(warehouse["_id"]),
            "name": warehouse["name"],
            "address": warehouse["address"],
            "created": warehouse["created"],
            "updated": warehouse["updated"],
            "active": warehouse["active"],
            "adminAsigned": str(warehouse["adminAsigned"])
        }
    for warehouse in warehouses]

 

def userAdminEntity(item) -> dict:
    warehouse_info = get_warehouse(str(item["_id"])) 

    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "lastname": item["lastname"],
        "email": item["email"],
        "created": item["created"].isoformat(),
        "updated": item["updated"].isoformat(),
        "active": item["active"],
        "is_admin": item["is_admin"],
        "warehouse": warehouse_info if warehouse_info else None
    }




def usersAdminEntity(entity) -> list:
    return[userAdminEntity(item) for item in entity if item ["active"]]

