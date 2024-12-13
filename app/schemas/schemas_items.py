def itemAdminEntity(item)->dict:
    return{
        "id":str(item["_id"]),
        "brand":str(item["brand"]),
        "model":item["model"],
        "sold_date":item.get("sold_date"),
        "out_of_stock":item["out_of_stock"],
        "created":item["created"], 
        "updated":item["updated"],
        "deleted":item["deleted"],
        "features":item["features"]
    }

def itemADminEntityAll(entity) -> list:
    return[itemAdminEntity(item) for item in entity]




def itemUserEntity(item)->dict:
    return{
        "id":str(item["_id"]),
        "model":item["model"],
        "sold_date":item["sold_date"],
        "out_of_stock":item["out_of_stock"],
        "features":item["features"]
    }


