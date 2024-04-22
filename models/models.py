from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    id_telegram = Column(Integer())
    name = Column(String())


class Key(Base):
    __tablename__ = 'keys'
    id = Column(Integer(), primary_key=True)
    title = Column(String())


class App(Base):
    __tablename__ = 'apps'
    id = Column(Integer, primary_key=True)
    title = Column(String(), unique=True)
    url = Column(String(), unique=True)
    launch_url = Column(String(), unique=True)
    counter = Column(Integer(), default=0)
