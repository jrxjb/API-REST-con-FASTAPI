from DataBase.DataBase import users_collection,item_collection
from bson import ObjectId

def get_admin_by_id(adminAsigned: str) -> dict:
    adminAsigned = users_collection.find_one({"_id": ObjectId(adminAsigned)})
    if adminAsigned:
        return {
            "id": str(adminAsigned["_id"]),
            "name": adminAsigned["name"],
            "lastname": adminAsigned["lastname"],
            "email": adminAsigned["email"],
            "active": adminAsigned["active"]
        }
    return {}

def get_all_Items(warehouse_id: str) -> list:
    items = item_collection.find({"warehouseid": ObjectId(warehouse_id)}) 
    if items is None:
        return []
    return [
        {
            "id": str(item["_id"]),
            "brand": item["brand"],
            "model": item["model"],
            "features": item["features"],
            "sold_date": item.get("sold_date"),
            "out_of_stock": item["out_of_stock"],
            "created": item["created"],
            "updated": item["updated"],
            "deleted": item["deleted"]
        }
        for item in items if not item["deleted"]
    ]



def warehouseEntity(item)->dict:
    
    admin_info = get_admin_by_id(str(item["adminAsigned"]))
    item_info = get_all_Items(str(item["_id"]))
    return{
        "id":str(item["_id"]),
        "name": str(item["name"]),
        "address":item["address"],
        "created":item["created"],
        "updated":item["updated"],
        "active": item["active"],
        "adminAsigned":admin_info,
        "items":item_info
    }

def warehouseEntityAll(entity) -> list:
    return[warehouseEntity(item) for item in entity if item["active"]]

def warehouseEntityUser(item)->dict:
    return{
        "id":str(item["_id"]),
        "name": str(item["name"]),
        "address":item["address"]
    }

