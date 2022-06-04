from sqlalchemy.sql.schema import ForeignKey
from authentication_and_db.database import Base
from sqlalchemy import Column,String,Integer,DateTime,Boolean
from sqlalchemy.orm import relationship


class Empikcode(Base):
    __tablename__ = 'empikcodes'

    id = Column(Integer,primary_key=True)
    code = Column(String)
    code_status = Column(Boolean,default=False)
    code_go = relationship('Codesharing',back_populates='codeempik',lazy='select',cascade = "all,delete")

    def __repr__(self):
        return "<empik code=%s)>" % (self.code)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    email = Column(String(40),unique=True)
    password = Column(String(100))
    card_number = Column(Integer,unique=True)
    code_go = relationship('Codesharing',back_populates='person',lazy='select',cascade = "all,delete")

    def __repr__(self):
        return "<user email=%s)>" % (self.email)

class Library(Base):
    __tablename__ = 'libraries'

    id = Column(Integer,primary_key=True)
    name = Column(String(40))
    email = Column(String(40),unique=True)
    password = Column(String(100))
    code_go = relationship('Codesharing',back_populates='library',lazy='select',cascade = "all,delete")

    def __repr__(self):
        return "<library name=%s)>" % (self.name)

class Empik(Base):

    __tablename__ = 'empiks'

    id = Column(Integer,primary_key=True)
    email = Column(String(40),unique=True)
    password = Column(String(100))

class Codesharing(Base):
    __tablename__ = 'codesharings'

    id = Column(Integer,primary_key=True)

    person_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    person = relationship('User',back_populates='code_go')

    code_id = Column(Integer,ForeignKey('empikcodes.id'),nullable=True)
    codeempik = relationship('Empikcode',back_populates='code_go')

    library_id = Column(Integer,ForeignKey('libraries.id'),nullable=False)
    library = relationship('Library',back_populates='code_go')

    register_date = Column(DateTime,nullable=True)

    # Having "nullable" as True will trigger automatic assignment of NULL when object is being created
    confirmation_date = Column(DateTime,nullable=True)
    pending_processing = Column(Boolean,default=True)


    def __repr__(self):
        return "<sharingID =%s status=%s>" % (self.id,self.pending_processing)



