from sqlalchemy import String, Column, Integer
from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    username = Column(String(30), nullable=False, unique=True, index=True)
    email = Column(String(300), nullable=False, unique=True)
    phone_number = Column(String(13), unique=True, nullable=False)
    password = Column(String)