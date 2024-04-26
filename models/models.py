from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """Класс определяющий структуру таблицы users в базе данных."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    id_telegram = Column(Integer())
    name = Column(String())


class Key(Base):
    """Класс определяющий структуру таблицы keys в базе данных."""
    __tablename__ = 'keys'
    id = Column(Integer(), primary_key=True)
    title = Column(String())


class App(Base):
    """Класс определяющий структуру таблицы apps в базе данных."""
    __tablename__ = 'apps'
    id = Column(Integer, primary_key=True)
    title = Column(String(), unique=True)
    url = Column(String(), unique=True)
    launch_url = Column(String(), unique=True)
    counter = Column(Integer(), default=0)


class UserApp(Base):
    """Класс определяющий структуру таблицы user_app в базе данных."""
    __tablename__ = 'user_app'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id', ondelete="CASCADE"))
    app_id = Column(Integer(), ForeignKey('apps.id', ondelete="CASCADE"))
