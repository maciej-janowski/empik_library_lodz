
from fastapi import HTTPException,status
from authentication_and_db import database,schemas,models
from authentication_and_db.hashing import Hash

def create_empik(request,db):

    # we use sql alchemy model we declared in "models" to create a new user and we pass the body of our request as variables
    new_empik = models.Empik(email=request.email,password=Hash.bcrypt(request.password))

    # we are adding new user to session
    db.add(new_empik)

    # we move data in our session to database
    db.commit()

    # and we refresh the current session so that we know the user is added
    db.refresh(new_empik)

    # we return the user
    return new_empik

def send_codes(codes,db,get_current_user):

    # check if logged user is empik
    if get_current_user['user_type'] == 'empik':

        # getting all codes sent
        list_of_codes = [models.Empikcode(code=x) for x in codes['card number']['codes']]
        
        # generating bulk upload
        db.bulk_save_objects(list_of_codes)
        db.commit()

        # returning all codes sent
        return (codes['card number']['codes'])

    # if not empik - return an exception that user is not authorized
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')


def get_empik_user(db,get_current_user):

    # check if logged user is empik
    if get_current_user['user_type'] == 'empik':

        # quering database (there is only one empik instance at the moment)
        empik_user = db.query(models.Empik).first()
        
        return empik_user

    # if not empik - return an exception that user is not authorized
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')


def get_all_codes(db,get_current_user):

    # check if logged user is empik
    if get_current_user['user_type'] == 'empik':

        # quering database
        all_codes = db.query(models.Empikcode).all()

        # returning codes from database
        return all_codes

    # if not empik - return an exception that user is not authorized
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')
