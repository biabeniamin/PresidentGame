#generated automatically
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session, validates
from sqlalchemy import *
from SqlAlchemy import Base, engine
from ValidationError import ValidationError

Session = sessionmaker(bind = engine, autocommit = False, autoflush = False)
session = scoped_session(Session)
def createDatabase():
	Base.metadata.bind = engine
	Base.metadata.create_all()
if __name__ == '__main__':
	createDatabase()
