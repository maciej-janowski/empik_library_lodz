from fastapi import APIRouter,Depends,status,Response,HTTPException,Path,Query,File,UploadFile,Form
from authentication_and_db import  database,schemas,models
from typing import List,Optional
from sqlalchemy.orm import Session
from functions import user_functions
from functions.authentication_functions import get_current_user
from dependencies import dir_path
import cv2
from PIL import Image
from io import BytesIO
import numpy as np




# we are declaring the tag for router
router = APIRouter(tags=['user'],
prefix='/user')

# declaring session for database
db:Session = Depends(database.get_db)


# def reading_card(card:Optional[bytes] = File(None)):
def reading_card(bytes_file:Optional[bytes] = File(None)):

        # if file was shared
        if bytes_file != None:

            # read bytes
            image_bytes = BytesIO(bytes_file).read()

            # get the array of pixes for shared image
            decoded = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
            
            # instance of QR detector
            det=cv2.QRCodeDetector()

            # get value from decoded file
            val, pts, st_code=det.detectAndDecode(decoded)

            # return card number
            return {'card number':val}
        else:
            return {'card_id':"no card detected"}
 

# docstring allows to add description on how the function works

@router.post('/create_user/',response_model=schemas.UserRegister)
def create_user(request:schemas.UserRegister,db=db):
    """
    Create a user with all information:

    - **email**: each user has to have unique email
    - **password**: password for all operations
    - **card_number**: card number will be fetched from QR code
    """
    return user_functions.create_user(request,db)

@router.get('/get_user/',response_model=schemas.UserDetails)
def get_library_user(db = db,name:str = None,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    """
    Get info on user

    Returned values are:
    - **email**: email used for authorization
    - **password**: returning hashed password
    
    """
    return user_functions.get_user(db,name,get_current_user)


@router.get('/get_user_requests/',response_model=List[schemas.Code_request_user])
def get_user_requests(user_id:int,db = db,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    """
    Get all requests raised by a user

    - **Returned values** => list of schemas for user requests
    
    """
    return user_functions.get_user_requests(user_id,db,get_current_user)

@router.post('/request_code')
def request_code(library_name:str,user_card:int = Depends(reading_card),db=db,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    """
    Create a request for code

    - **Necessary content** => qr code of the card user is assigned to
    
    """
    return user_functions.request_code(library_name,user_card,db,get_current_user)

@router.get('/test_authentication')
def test_authentication(db=db,get_current_user:schemas.UserDetails = Depends(get_current_user)):
    return user_functions.test_authentication(db,get_current_user)