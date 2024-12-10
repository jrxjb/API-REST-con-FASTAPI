from typing import List,Any,Dict

def userEntity(item: Dict[str, Any]) -> Dict[str, Any]:
    return{
        "id":str(item["_id"]),
        "name":item["name"],
        "lastname":item["lastname"],
        "email":item["email"],
        "created":item["created"].isoformat(),
        "updated":item["updated"].isoformat(),
        "active":item["active"]
    }

def usersEntity(entity: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return[userEntity(item) for item in entity]
