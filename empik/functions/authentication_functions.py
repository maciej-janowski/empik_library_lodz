from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from authentication_and_db import JWTtoken

# below we are declaring the route from which token will be sent(generation will happen)
ouath2_scheme = OAuth2PasswordBearer(tokenUrl='authentication/login',
scopes={"empik": "user authenticated to perform empik requests",
"reader":'user authenticated to perform user requests',
"library":'user authenticated to perform library requests'})
# ouath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# function for checking the credentials
def get_current_user(token:str=Depends(ouath2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # we are returning the result of the function for verification
    return JWTtoken.verify_token(token,credentials_exception)