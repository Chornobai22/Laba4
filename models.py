from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key = True)
    name = Column(String(45), nullable = False)
    surname = Column(String(45), nullable = False)
    username = Column(String(45), nullable = False)
    password = Column(String(1000))
    accessusers = Column(String(45))
    children3 = relationship("Rating")
    def __repr__(self):
        return f"{self.id}, {self.name}, {self.surname}, {self.username}, {self.password},{self.accessusers} "


class Student(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key = True)
    firstname = Column(String(45), nullable = False)
    surname = Column(String(45), nullable = True)
    course = Column(Integer, nullable = True)
    best_grade = Column(Integer)
    children = relationship("Rating")

    def __repr__(self):
        return f"{self.id}, {self.firstname}, {self.surname}, {self.course}, {self.best_grade} "

class Rating(Base):
    __tablename__ = "Rating"

    id = Column(Integer, primary_key = True)
    title = Column(String(45), nullable = False)
    Student_id = Column(Integer, ForeignKey('Student.id'))
    user_creator_id = Column(Integer, ForeignKey('User.id'))

    def __repr__(self):
        return f"{self.id}, {self.title}, {self.Student_id}, {self.accessus} "

class Properties(Base):
    __tablename__ = "Propeties"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    rating_id = Column(Integer, ForeignKey('Rating.id'))
    children1 = relationship("Rating")
    children2 = relationship("User")

    def __repr__(self):
        return f"{self.id}, {self.user_id}, {self.rating_id} "


