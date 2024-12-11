from fastapi import FastAPI
from routers.crud_user import user
from routers.login import appL
app= FastAPI()

#user
app.include_router(user)
app.include_router(appL)
