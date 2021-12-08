from tests.conftest import *
from flask import jsonify


def test_add_student(client, login_User):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']

    }
    res = client.post('/student',headers = headers, json=student1)
    assert res.status_code == 403
    student1['created'] = login_User['new_user_id']
    wrong_student2['created']  = login_User['new_user_id']
    res = client.post('/student', headers=headers, json=wrong_student2)
    assert res.status_code == 422
    res = client.post('/student', headers=headers, json=student1)
    assert res.status_code == 200
    student1['created'] = -1
    wrong_student2['created'] = -1
    s.query(Student).delete()
    s.query(User).delete()


def test_get_all_student(client, login_User):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']
    }
    res = client.get('/student',headers = headers)
    assert res.status_code == 200
    s.query(Student).delete()
    s.query(User).delete()

    #print(res.get_json


def test_get_student_grade(client, login_User, Student_C):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']

    }
    #res = client.get('/student/grade/1426437',headers = headers)
    #assert res.status_code == 404
    #res = client.get('/student/grade/777',headers = headers)
    #assert res.get_json() == {"message": "Student could not be found."}
    res = client.get(f'/student/grade/{Student_C.best_grade}', headers=headers)
    assert res.status_code == 200
    s.query(Student).delete()
    s.query(User).delete()

def test_get_student(client, login_User, Student_C):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']

    }
    res = client.get('/student/0',headers = headers)
    assert res.get_json() == {"message": "Student could not be found."}
    res = client.get(f'/student/{Student_C.id}', headers=headers)
    assert res.status_code == 200
    s.query(Student).delete()
    s.query(User).delete()

def test_put_student(client, Student_C_login, login_User, Student_C):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']
    }
    res = client.put(f'/student/{Student_C.id}',headers = headers, json = student_without_id)
    #assert res.status_code == 403
    assert res.get_json() == {'message': 'Access denied'}
    res = client.put(f'/student/{Student_C_login.id}', headers=headers, json = student_without_id)
    assert res.status_code == 403


    student1['created'] = login_User['new_user_id']
    res = client.put(f'/student/{Student_C_login.id}', headers=headers, json = student1)
    assert res.status_code == 400
    student1['created'] = -1
    student_without_id['created'] = login_User['new_user_id']
    res = client.put(f'/student/{Student_C_login.id}', headers=headers, json=student_without_id)
    assert res.status_code == 200
    student_without_id['created'] = -1
    s.query(Student).delete()
    s.query(User).delete()


def test_delete_student(client, Student_C_login, login_User, Student_C):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']
    }
    res = client.delete(f'/student/{Student_C.id}',headers = headers)
    assert res.status_code == 403

    res = client.delete(f'/student/0', headers=headers)
    assert res.status_code == 404

    res = client.delete(f'/student/{Student_C_login.id}', headers=headers)

    assert res.status_code == 200
    s.query(Student).delete()
    s.query(User).delete()
