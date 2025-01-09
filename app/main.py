from fastapi import FastAPI
from routers.crud_user import user
from routers.login import appL
from routers.crud_items import items
from routers.create_admin import admin
from routers.crud_warehouse import warehouse
app= FastAPI()

#user
app.include_router(user)
app.include_router(appL)
app.include_router(items)
app.include_router(admin)
app.include_router(warehouse)
