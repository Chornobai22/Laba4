import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from routes import b
from app import app
from check import engine, s
from models import Base
from flask import Flask
#from flask_pytest_example.handlers.routes import configure_routes
from schemas import *

user_user = {"id":1, "name":"f", "surname":"s", "username":"User_A", "password":"1", "accessusers":"User"}
user_admin = {"id":2, "name":"f", "surname":"s", "username":"Admin_A", "password":"1", "accessusers":"Admin"}
wrong_user = {"id":3, "name":"f", "surname":"s", "username":"username3_A", "password":"1", }
Abslut_wrong_user = { "id":3,"name":"f", "surname":"s", "username":"Admin_A","accessusers":"Admin" }
user_without_id = {"name":"f", "surname":"s", "username":"username3", "password":"1","accessusers":"Admin" }
wrong_user_without_id = {"name":"f", "username":"username3","accessusers":"Admin" }
@pytest.fixture(scope="session")
def client():
    s.query(Rating).delete()
    s.query(Student).delete()
    s.query(User).delete()
    client = app.test_client()
    yield client
    s.query(Rating).delete()
    s.query(Student).delete()
    s.query(User).delete()
    s.commit()

@pytest.fixture()
def user_C():
    User_c = User(id=3, name="username1",  username = "User", surname="username1",
                password="1", accessusers="User")
    s.add(User_c)
    s.commit()
    return User_c
'''
@pytest.fixture()
def admin_C():
    User_c = User(id=4, name="f",  username = "Admin", surname="username1",
                password="1", accessusers="Admin")
    s.add(User_c)
    s.commit()
    return User_c
'''

@pytest.fixture()
def login_User(client):
    #s.query(User).delete()
    beck = user_user['username']
    user_user['username'] = beck + str(user_user['id'])
    res = client.post('/register', json=user_user)
    user_user['username'] = beck
    return res.get_json()

@pytest.fixture()
def login_Admin(client):
    res = client.post('/register', json=user_admin)
    return res.get_json()


student1= {"id":1, "firstname":"f", "surname":"s", "course":4, "best_grade":4, "created":0}
student2 = {"id":2, "firstname":"f", "surname":"s", "course":4, "best_grade":4, "created":0}
wrong_student2 = {"id":2, "course":4, "best_grade":4, "created":0}
student_without_id = { "firstname":"f", "surname":"s", "course":4, "best_grade":4, "created":0}
wrong_student_without_id = { "firstname":"f", "surname":"s", "course":4, "best_grade":4, "created":0}
@pytest.fixture()
def Student_C(user_C):
    Student_c = Student(id=3, firstname="f",
                        surname = "s", course=4,
                        created = user_C.id, best_grade=1)
    s.add(Student_c)
    s.commit()
    return Student_c

@pytest.fixture()
def Student_C_login(login_User):
    Student_c = Student(id=4, firstname="f",
                        surname = "s", course=4,
                        created = login_User['new_user_id'], best_grade=1)
    s.add(Student_c)
    s.commit()
    return Student_c


reting1 = {"id":3, "title":"f", "Student_id":0, "user_creator_id":0}
reting_without = {"title":"f", "Student_id":0, "user_creator_id":0}
@pytest.fixture()
def Rating_C(Student_C , user_C):
    Rating_c = Rating(title = 'f',Student_id = Student_C.id, user_creator_id =  user_C.id)
    s.add(Rating_c)
    s.commit()
    return Rating_c

@pytest.fixture()
def Rating_C_login(login_Admin, Student_C):

    Rating_c = Rating(id = 5, title = 'f',Student_id = Student_C.id, user_creator_id = login_Admin['new_user_id'])
    s.add(Rating_c)
    s.commit()
    return Rating_c