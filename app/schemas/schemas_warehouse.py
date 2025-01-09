def warehouseEntity(item)->dict:
    return{
        "id":str(item["_id"]),
        "name": str(item["name"]),
        "address":item["address"],
        "created":item["created"],
        "updated":item["updated"],
        "active": item["active"],

    }

def warehouseEntityAll(entity) -> list:
    return[warehouseEntity(item) for item in entity]

def warehouseEntityUser(item)->dict:
    return{
        "id":str(item["_id"]),
        "name": str(item["name"]),
        "address":item["address"]
    }

