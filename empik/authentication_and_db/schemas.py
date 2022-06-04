
from datetime import datetime,date
from typing import Optional
from pydantic import BaseModel,Field




# declaring models for registering in database

class UserRegister(BaseModel):
    email:str
    password:str
    card_number:int
    class Config():
        orm_mode=True
        schema_extra = {
            "example": {
                "email": "user@email.com",
                "password": "Use_strong_password",
                "card_number": "Card_number_received_during_visit_at_library"
            }
        }

class UserDetails(BaseModel):
    email:str
    card_number:int
    class Config():
        orm_mode=True

class Library(BaseModel):
    name:str
    email:str
    password:str
    class Config():
        orm_mode=True
        

class LibraryRegister(BaseModel):
    name:str
    email:str
    password:str
    class Config():
        orm_mode=True
        schema_extra = {
            "example": {
                "name": "Name_of_the_library",
                "email": "library@email.com",
                "password": "Use_strong_password",
            }
        }

class EmpikRegister(BaseModel):
    email:str
    password:str
    class Config():
        orm_mode=True
        schema_extra = {
            "example": {    
                "email": "empik@email.com",
                "password": "Use_strong_password",
            }
        }

class EmpikLogin(BaseModel):
    id:int
    email:str
    password:str
    class Config():
        orm_mode=True

class Code(BaseModel):
    id:int
    code:str
    # code_status:bool
    code_status:bool = Field(..., alias='code_used')
    class Config():
        orm_mode=True
        allow_population_by_field_name = True

class Code_only(BaseModel):
    code:str
    class Config():
        orm_mode=True
  


# declaring schema for Code request
class Code_request(BaseModel):
    id:int = Field(...,alias='request_id')
    register_date: datetime
    pending_processing: bool
    person: UserDetails = Field(..., alias='library_user')
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

# declaring schema for Code request
class Code_request_user(BaseModel):
    id:int = Field(...,alias='request_id')
    register_date: datetime
    pending_processing: bool
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# declaring schema for users with code
class Code_request_status(BaseModel):
    id:int = Field(...,alias='request_id')
    register_date: datetime
    pending_processing: bool
    # using "Field" allows to overwrite the key that we use. So instead of "person" we will see "library_user"
    person: UserDetails = Field(..., alias='library_user')
    codeempik: Code_only = Field(...,alias='code_assigned')
    class Config:
        orm_mode = True
        allow_population_by_field_name = True