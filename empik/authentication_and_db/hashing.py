from passlib.context import CryptContext

# schema for encryption
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# creating a class for encryption
class Hash():
    # encrypting the password by sending the password to function
    def bcrypt(password: str):
        # returning hashed password
        return pwd_cxt.hash(password)

# verifying password
    def verify(plain_password,hashed_password):
        # returning verification
        return pwd_cxt.verify(plain_password,hashed_password)