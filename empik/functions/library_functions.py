from authentication_and_db import database,schemas,models
from authentication_and_db.hashing import Hash
from fastapi import status,HTTPException
import datetime
from sqlalchemy import and_

def create_library(request,db):

    # we use sql alchemy model we declared in "models" to create a new user and we pass the body of our request as variables
    new_library = models.Library(name=request.name,email=request.email,password=Hash.bcrypt(request.password))

    # we are adding new user to session
    db.add(new_library)

    # we move data in our session to database
    db.commit()

    # and we refresh the current session so that we know the user is added
    db.refresh(new_library)

    # we return the user
    return new_library

def get_library_user(db,name,get_current_user):

    # check if logged user is library
    if get_current_user['user_type'] == 'library':

        library = db.query(models.Library).filter(models.Library.name==name).first()

        return library

    # if not library - return an exception that user is not authorized
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')


def get_code_requests_stats(db,name,get_current_user):

    # check if logged user is library
    if get_current_user['user_type'] == 'library':

        # first we are quering codesharing table and then we join it with library table. Next - we filter created table on name of the library
        all_codes = db.query(models.Codesharing).join(models.Library).filter(models.Library.name == name).all()
        print(all_codes)
        # returning all codes found
        return all_codes
    
    # if not library - return an exception that user is not authorized
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')


def verify_code(request_id,accepted,db,get_current_user):

    # check if logged user is library
    if get_current_user['user_type'] == 'library':
    
        # getting the request for code
        processed_request = db.query(models.Codesharing).filter(models.Codesharing.id ==request_id)

        # checking if request is accepted:
        if not accepted:
            processed_request.update({"confirmation_date":datetime.datetime.utcnow(),"pending_processing":False})
            db.commit()
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,detail=f'Request for Empik code has been rejected by the library.')

        else:
            # check first available code
            available_code = db.query(models.Empikcode).filter(models.Empikcode.code_status == False).all()
            
            # if codes are not available
            if len(available_code) == 0:
                
                # close the request by updating fields in database
                processed_request.update({"confirmation_date":datetime.datetime.utcnow(),"pending_processing":False})
                db.commit()

            # inform about it and return an Exception
                raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY,detail='There are no codes available. Please check next month')
            else:
            # if code available - get id of the first code in the list
                print(available_code[0].id)
                code_assigned = available_code[0].code
                available_code = available_code[0].id
            
            
            # finding user id based on card number
            empik_code_request = db.query(models.Codesharing).filter(models.Codesharing.id == request_id)

            empik_code_request.update({'code_id':available_code,'confirmation_date':datetime.datetime.utcnow(),'pending_processing':False})

            db.query(models.Empikcode).filter(models.Empikcode.id == available_code).update({'code_status':True})

            # we move data in our session to database
            db.commit()

            # returning a message that request was generated
            return {"Code assigned":"%s" % (str(code_assigned))}
    
    # if not library - return an exception that user is not authorized
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')

    
def users_code_assignment(having_code,name,db,get_current_user):

    # check if logged user is library
    if get_current_user['user_type'] == 'library':

        # checking if we want users with codes assigned or without
        if having_code:
            all_codes = db.query(models.Codesharing).join(models.Library).filter(and_(models.Library.name == name,models.Codesharing.code_id != False)).all()
        else:
            all_codes = db.query(models.Codesharing).join(models.Library).filter(and_(models.Library.name == name,models.Codesharing.code_id != True)).all()
        return all_codes

    # if not library - return an exception that user is not authorized
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')
