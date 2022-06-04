from fastapi import APIRouter,Depends,status,Response,HTTPException,Path,Query,File,UploadFile,Form
from authentication_and_db import  database,schemas,models
from typing import List,Optional
from sqlalchemy.orm import Session
from functions import user_functions
from functions.authentication_functions import get_current_user
from dependencies import dir_path
from authentication_and_db.hashing import Hash
from authentication_and_db import JWTtoken
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordRequestFormStrict


# we are declaring the tag for router
router = APIRouter(tags=['authentication'],
prefix='/authentication')

@router.post('/login')
# def getting_token(request:OAuth2PasswordRequestFormStrict = Depends(),db:Session = Depends(database.get_db)):
def getting_token(request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):

    # looking for user
    print('request',request)
    print('request_scopes',request.scopes[0])

    # checking which user logged in
    user = db.query(models.User).filter(models.User.email==request.username).first()

    empik = db.query(models.Empik).filter(models.Empik.email==request.username).first()

    library = db.query(models.Library).filter(models.Library.email==request.username).first()

    # assigning user
    user = next(item for item in [user,empik,library] if item is not None)
    print(user)

    # if user is not found in all 3 cases
    if not user:

        # return an exception that user does not exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No user with name {request.username} found")

        # check the password
    if not Hash.verify(request.password,user.password):

        # if password is wrong - raise an exception
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Invalid credentials")
    
    # assign role
    # getting the token
    access_token = JWTtoken.create_access_token(data={"sub": user.email,"user_type":request.scopes[0]})

    return {"access_token": access_token, "token_type": "bearer"}