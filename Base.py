from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from Models import *


#Create an engine to the database
engine = create_engine('mysql+pymysql://root:Davemurray33@localhost/chromaffin')

Session = sessionmaker(bind=engine)

Base = declarative_base()


