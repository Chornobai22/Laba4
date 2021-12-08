from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt
from check import *

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    surname = Column(String(45), nullable=False)
    username = Column(String(45), nullable=False)
    password = Column(String(1000), nullable=False)
    accessusers = Column(String(45), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.surname = kwargs.get('surname')
        self.username = kwargs.get('username')
        self.password = bcrypt.hash(kwargs.get('password'))
        self.accessusers = kwargs.get('accessusers')

    def get_token(self, expire_time=0.01):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, username, password):
        user = s.query(User).filter_by(username=username).first()
        if not bcrypt.verify(password, user.password):
            return False
        return user

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.surname}, {self.username}, {self.password},, {self.accessusers}"


class Student(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(45), nullable=False)
    surname = Column(String(45), nullable=True)
    course = Column(Integer, nullable=True)
    best_grade = Column(Integer)
    created = Column(Integer, ForeignKey('User.id'), nullable=False)

    User = relationship("User")

    def __repr__(self):
        return f"{self.id}, {self.firstname}, {self.surname}, {self.course}, {self.best_grade},{self.created} "


class Rating(Base):
    __tablename__ = "Rating"

    id = Column(Integer, primary_key=True)
    title = Column(String(45), nullable=False)
    Student_id = Column(Integer, ForeignKey('Student.id'))
    user_creator_id = Column(Integer, ForeignKey('User.id'))

    Student = relationship("Student")
    User = relationship("User")

    def __repr__(self):
        return f"{self.id}, {self.title}, {self.Student_id}, {self.accessus},{self.user_creator_id} "


class TokenBlockList(Base):
    __tablename__ = "token_block_list"

    id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False)
    created_at = Column(DateTime, nullable=False)
