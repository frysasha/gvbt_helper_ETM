from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

CONNECTION_ROW = "sqlite:///robots.db"

BaseModel = declarative_base(name='BaseModel')

engine = create_engine(CONNECTION_ROW)

Session = sessionmaker(engine, autoflush=False, autocommit=False)
session = Session()

