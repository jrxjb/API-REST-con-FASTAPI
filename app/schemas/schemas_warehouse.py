def warehouseEntity(item)->dict:
    return{
        "id":str(item["_id"]),
        "name": str(item["name"]),
        "address":item["address"],
        "created":item["created"],
        "updated":item["updated"],
        "active": item["active"],
        "adminAsigned":item["adminAsigned"]

    }

def warehouseEntityAll(entity) -> list:
    return[warehouseEntity(item) for item in entity if item["active"]]

def warehouseEntityUser(item)->dict:
    return{
        "id":str(item["_id"]),
        "name": str(item["name"]),
        "address":item["address"]
    }

