
from fastapi import FastAPI

from  authentication_and_db import models




from fastapi import FastAPI
from authentication_and_db.database import engine
# we need session so the connection with our database
from sqlalchemy.orm import Session


from routers import empik_router,user_router,library_router,authentication_router




app = FastAPI()




app.include_router(user_router.router)
app.include_router(library_router.router)
app.include_router(empik_router.router)
app.include_router(authentication_router.router)


# everytime app is run it will create tables if they are not present in the database
models.Base.metadata.create_all(bind=engine)








