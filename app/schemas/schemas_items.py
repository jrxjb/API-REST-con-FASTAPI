from DataBase.DataBase import warehouse_collection
from bson import ObjectId

def get_warehouse_by_id(warehouse: str) -> dict:
    warehouse = warehouse_collection.find_one({"_id": ObjectId(warehouse)})
    if warehouse:
        return {
            "id": str(warehouse["_id"]),
            "name": warehouse["name"],
            "address": warehouse["address"],
            "adminAsigned": warehouse["adminAsigned"]
        }
    return {}




def itemAdminEntity(item)->dict:
    warehouse_info = get_warehouse_by_id(item["warehouse"])
    return{
        "id":str(item["_id"]),
        "brand":str(item["brand"]),
        "model":item["model"],
        "sold_date":item.get("sold_date"),
        "out_of_stock":item["out_of_stock"],
        "created":item["created"], 
        "updated":item["updated"],
        "deleted":item["deleted"],
        "features":item["features"],
        "warehouse": warehouse_info
    }

def itemADminEntityAll(entity) -> list:
    return[itemAdminEntity(item) for item in entity if not item["deleted"]]


def itemUserEntity(item)->dict:
    return{
        "id":str(item["_id"]),
        "model":item["model"],
        "sold_date":item["sold_date"],
        "out_of_stock":item["out_of_stock"],
        "features":item["features"]
    }


def itemEntityAllUser(entity) -> list:
    return[itemUserEntity(item) for item in entity if item["deleted"]]