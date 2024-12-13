from fastapi import FastAPI
from routers.crud_user import user
from routers.login import appL
from routers.crud_items import items
app= FastAPI()

#user
app.include_router(user)
app.include_router(appL)
app.include_router(items)
