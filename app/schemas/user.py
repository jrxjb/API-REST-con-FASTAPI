from schemas.schemas_warehouse import warehouseEntity
from DataBase.DataBase import warehouse_collection
from bson import ObjectId

def userEntity(item) -> dict:
    if item.get("warehouse"):
        warehouse_info = get_warehouse(str(item["_id"]))
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

