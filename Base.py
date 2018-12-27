from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


file = open("config.txt", "r")

infos=file.readlines()


#Create an engine to the database
engine = create_engine(
    'mysql+pymysql://root:%s@localhost/%s' % (infos[1][9:], infos[0][14:-1]))

Session = sessionmaker(bind=engine)

Base = declarative_base()


