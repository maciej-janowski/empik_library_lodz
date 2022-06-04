from urllib import response
from fastapi import APIRouter,Depends,status,Response,HTTPException,Path,Query,File,UploadFile,Form
from authentication_and_db import  database,schemas,models
from typing import List,Optional
from sqlalchemy.orm import Session
from functions import user_functions
from functions import library_functions
from functions.authentication_functions import get_current_user
from dependencies import dir_path


# we are declaring the tag for router
router = APIRouter(tags=['library'],
prefix='/library')

# declaring session for database
db:Session = Depends(database.get_db)


# getting info on all codes
@router.get('/code_requests_stats/',response_model=List[schemas.Code_request])
def code_requests_stats(db = db,name:str = None,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    return library_functions.get_code_requests_stats(db,name,get_current_user)



@router.post('/create_library_user/',response_model=schemas.LibraryRegister)
def create_library_user(request:schemas.LibraryRegister,db = db):
    return library_functions.create_library(request,db)

@router.get('/get_library/',response_model=schemas.Library)
def get_library_user(db = db,name:str = None,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    return library_functions.get_library_user(db,name,get_current_user)

@router.get('/verify_code/')
def verify_code(request_id:int,accepted:int,db = db,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    return library_functions.verify_code(request_id,accepted,db,get_current_user)

@router.get('/users_code_assignment',response_model=List[schemas.Code_request_status])
def users_code_assignment(having_code:int,name:str,db = db,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    return library_functions.users_code_assignment(having_code,name,db,get_current_user)

# @router.get('/get_specific_user/{id}',response_model=schemas.UserDetails)
# def get_specific_user(id:int,value:int,db:Session = Depends(database.get_db)):
#     return user_functions.getting_specific_user(id,db,value)