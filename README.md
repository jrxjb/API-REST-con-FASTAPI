# FastAPI con mongoDB

## Requisitos del Proyecto

Para ejecutar este proyecto, necesitas las siguientes dependencias. Puedes instalarlas utilizando `pip`.

### Dependencias

```plaintext
annotated-types==0.7.0
anyio==4.7.0
bcrypt==4.0.1
click==8.1.7
colorama==0.4.6
dnspython==2.7.0
ecdsa==0.19.0
fastapi==0.115.6
h11==0.14.0
idna==3.10
passlib==1.7.4
pyasn1==0.6.1
pydantic==2.10.3
pydantic_core==2.27.1
pymongo==4.10.1
python-dotenv==1.0.1
python-jose==3.3.0
python-multipart==0.0.19
rsa==4.9
six==1.17.0
sniffio==1.3.1
starlette==0.41.3
typing_extensions==4.12.2
uvicorn==0.32.1
```


## Configuración de Variables de Entorno

Para ejecutar este proyecto, necesitas definir las siguientes variables de entorno en un archivo `.env`. Aquí está el detalle de cada variable que debes configurar:

### Variables de Entorno

- `SECRET_KEY`: Tu clave secreta utilizada para codificar y decodificar tokens JWT.
- `ALGORITHM`: El algoritmo utilizado para codificar y decodificar tokens JWT (por ejemplo, "HS256").
- `PEPPER`: Tu clave adicional para aumentar la seguridad de las contraseñas.
- `MONGO_URL`: La URL de conexión a tu base de datos MongoDB.
- `DATABASE_NAME`: El nombre de tu base de datos.
- `COLLECTION_NAME`: El nombre de tu colección en la base de datos.

### Ejemplo de Archivo `.env`

```env
SECRET_KEY="your_secret_key_here"
ALGORITHM="your_algorithm_here"
PEPPER="your_pepper_here"
MONGO_URL="your_mongo_url_here"
DATABASE_NAME="your_database_name_here"
COLLECTION_NAME="your_collection_name_here"
```



