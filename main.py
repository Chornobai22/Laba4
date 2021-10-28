from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class user(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    name = Column(String(45), nullable = False)
    surname = Column(String(45), nullable = True)
    username = Column(String(45), nullable = True)
    password = Column(String(45), nullable = True)
    accessusers = Column(String(45), nullable = True)
    # Gravities = relationship("Gravity", backref = "FV", lazy = "dynamic")
class Student(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key = True)
    firstname = Column(String(45), nullable = False)
    surname = Column(String(45), nullable = True)
    course = Column(Integer, nullable = True)
    best_grade = Column(Integer)
    children = relationship("Rating")


class Rating(Base):
    __tablename__ = "Rating"

    id = Column(Integer, primary_key = True)
    title = Column(String(45), nullable = False)
    Student_id = Column(Integer, ForeignKey('Student.id'))
    accessus = Column(String(45), nullable = True)

# class Gravity(Base):
#     __tablename__ = "Gravity"
#     GravityId = Column(Integer, primary_key = True)
#     FvId = Column(Integer, ForeignKey("Fv.FvId"), nullable = False)
#     Gravity = Column(Float, nullable = False)
#     Timestamp = Column(DATETIME(fsp = 6), nullable = False)
