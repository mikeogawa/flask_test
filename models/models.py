from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime

class FoodDB(Base):
    __tablename__ = "foodDB"
    id = Column(Integer, primary_key=True)
    title = Column(String(128),unique=True)
    body = Column(Text)
    expire = Column(DateTime)
    date = Column(DateTime, default=datetime.now())


    def __init__(self,title=None, body=None, expire=None, date=None):
        self.title = title
        self.body = body
        self.expire = expire
        self.date = date

    @property
    def exp(self):
        return self.expire.strftime('%Y-%m-%d')

    @property
    def rec(self):
        return self.date.strftime('%Y-%m-%d')

    @property
    def is_expired(self):
        return self.expire < self.date


class User(Base):
    __tablename__ = "userDB"
    id = Column(Integer, primary_key=True)
    user = Column(String(128), unique=True)
    password = Column(String(128))

    def __init__(self, user=None, password=None):
        self.user = user
        self.password = password
