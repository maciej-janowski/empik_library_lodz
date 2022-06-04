from fastapi import APIRouter,Depends,status,Response,HTTPException,Path,Query,File,UploadFile,Form
from authentication_and_db import  database,schemas,models
from typing import List,Optional
from sqlalchemy.orm import Session
from functions import empik_functions
from functions.authentication_functions import get_current_user
from dependencies import dir_path
import pandas as pd
from io import BytesIO


# we are declaring the tag for router
router = APIRouter(tags=['empik'],
prefix='/empik')

# declaring session for database
db:Session = Depends(database.get_db)

def common_parameters(bytes_file:Optional[bytes] = File(None)):
    if bytes_file != None:
        df = pd.read_csv(BytesIO(bytes_file))
        return {'card number':df}
    else:
        return {'Error':'No file passed'}


@router.post('/pandas_reading/')
def send_codes(codes: dict = Depends(common_parameters),db = db,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    return empik_functions.send_codes(codes,db,get_current_user)


@router.post('/create_empik_user/',response_model=schemas.EmpikRegister)
def create_empik_user(request:schemas.EmpikRegister,db=db):
    return empik_functions.create_empik(request,db)


@router.get('/get_empik_user/',response_model=schemas.EmpikLogin)
def get_empik_user(db=db,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    return empik_functions.get_empik_user(db,get_current_user)


# @router.get('/get_all_codses/')
@router.get('/get_all_codes/',response_model=List[schemas.Code])
def get_all_codes(db=db,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    return empik_functions.get_all_codes(db,get_current_user)
