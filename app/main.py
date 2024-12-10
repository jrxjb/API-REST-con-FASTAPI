from fastapi import FastAPI
from routers.crud_user import user
app= FastAPI()

#user
app.include_router(user)


@app.get('/hola')
async def hola():
    return "hola"


