from datetime import datetime, timedelta
from jose import JWTError, jwt
from authentication_and_db import schemas
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
# alorithm used
ALGORITHM = os.getenv("ALGORITHM")
# ALGORITHM = "HS256"
# how long token works
ACCESS_TOKEN_EXPIRE_MINUTES = 5


def create_access_token(data: dict):

    # copying the data passed
    to_encode = data.copy()
    print('to_encode_data',to_encode)

    # setting up time for expiration
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print('expire_data',expire)

    # updating the info on expiration
    to_encode.update({"exp": expire})

    # encoding
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # returing token
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        # decoding what is inside token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # checking name
        naming: str = payload.get("sub")

        print('getting payload',payload.get('user_type'))
        user_type: str = payload.get('user_type')

        # if name is None
        if naming is None:

            # raise exeception
            raise credentials_exception

        # otherwise return token data/confirmation
        token_data = {'detail':"User authorized", 'user_type':user_type}
        return token_data
    
    # something failed => raise exception
    except JWTError:
        raise credentials_exception