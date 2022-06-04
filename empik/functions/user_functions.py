from fastapi import status,HTTPException
from matplotlib.pyplot import get
from sqlalchemy import false
from authentication_and_db import database,schemas,models
from authentication_and_db.hashing import Hash
import datetime



def create_user(request,db):

    # we use sql alchemy model we declared in "models" to create a new user and we pass the body of our request as variables
    new_user = models.User(email=request.email,password=Hash.bcrypt(request.password),card_number=request.card_number)

    # we are adding new user to session
    db.add(new_user)

    # we move data in our session to database
    db.commit()

    # and we refresh the current session so that we know the user is added
    db.refresh(new_user)

    # we return the user
    return new_user


def get_user(db,name,get_current_user):

    # check the user type
    if get_current_user['user_type'] == 'reader':

        # quering database
        user = db.query(models.User).filter(models.User.email == name).first()

        # returning user
        return user

    else:

        # if not reader - raise an exception about not being authorized to make a request
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')  


def request_code(library_name,user_card,db,get_current_user):

    # check the user type
    if get_current_user['user_type'] == 'reader':

        # finding user id based on card number
        user_id = db.query(models.User).filter(models.User.card_number == int(user_card['card number'])).first().id

        # checking if there a request for user already
        last_request = db.query(models.Codesharing).join(models.User).filter(models.User.id == user_id).order_by(models.Codesharing.id.desc()).first()
        
        # if there is a request pending processing - infor user about it
        if last_request.pending_processing == True:
            return {"status":"One request already pending confirmation. You cannot request two codes"}

        # if user already received code and 30 days hasn't passed since that moment - return information with how many days user needs to wait to submit another request
        elif last_request.code_id and (datetime.datetime.now() - last_request.confirmation_date).days < 30:
            
            return {'status':f'You can get only one code for 30 days. Next request possible in {30 - (datetime.datetime.now() - last_request.confirmation_date).days} day/s'}

        
        # finding library id based on library name
        library_id = db.query(models.Library).filter(models.Library.name == library_name).first().id

        # new_sharing = models.Codesharing(person_id=user_id,library_id=library_id,code_id=available_code,register_date=datetime.datetime.utcnow())

        new_sharing = models.Codesharing(person_id=user_id,library_id=library_id,register_date=datetime.datetime.utcnow())

        # we are adding new user to session
        db.add(new_sharing)

        # we move data in our session to database
        db.commit()

        # returning a message that request was generated
        return {"status":"Code requested. Library verifying request"}
    else:

        # if not reader - raise an exception about not being authorized to make a request
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')  

def get_user_requests(user_id,db,get_current_user):
    
    # check the user type
    if get_current_user['user_type'] == 'reader':

        # querying all requests of a user
        all_requests = db.query(models.Codesharing).join(models.User).filter(models.User.id == user_id).all()
        print(all_requests)

        # returning all requests found
        return all_requests
    else:

        # if not reader - raise an exception about not being authorized to make a request
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')


def test_authentication(db,get_current_user):
    if get_current_user['user_type'] == 'reader':
        print('db',db)
        print('get_current_user',get_current_user)
        print('details of function',get_current_user['detail'])
        print('details of function',get_current_user['user_type'])
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail='Token properly processed')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to perform request')