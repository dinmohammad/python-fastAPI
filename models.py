from sqlalchemy.types import String, Integer
from sqlalchemy.schema import Column
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    age = Column(Integer)
    year = Column(String(50))

