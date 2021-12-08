from tests.conftest import *
from flask import jsonify


def test_get_all_reting(client, login_User):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']
    }

    res = client.get('/rating', headers=headers)
    assert res.status_code == 200
    s.query(Rating).delete()
    s.query(Student).delete()
    s.query(User).delete()



def test_add_reting(client, login_User, login_Admin , Student_C):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']
    }
    res = client.post('/rating',headers = headers, json=reting1)
    assert res.status_code == 403
    reting1['user_creator_id'] = login_User['new_user_id']
    res = client.post('/rating', headers=headers, json=reting1)
    assert res.status_code == 404
    reting1['Student_id'] = Student_C.id
    res = client.post('/rating', headers=headers, json=reting1)
    assert res.status_code == 406
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_Admin['access_token']
    }
    reting1['user_creator_id'] = login_Admin['new_user_id']
    res = client.post('/rating', headers=headers, json=reting1)
    assert res.status_code == 200
    reting1['Student_id'] = 0
    reting1['user_creator_id'] = 0
    s.query(Rating).delete()
    s.query(Student).delete()
    s.query(User).delete()



def test_put_reting(client, Rating_C_login, login_User, login_Admin, Student_C):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']
    }
    res = client.put('/rating/0',headers = headers, json = reting1)
    assert res.status_code == 404
    #assert res.get_json() == ""
    res = client.put(f'/rating/{Rating_C_login.id}', headers=headers, json = reting1)
    assert res.status_code == 400

    res = client.put(f'/rating/{Rating_C_login.id}', headers=headers, json=reting_without)
    assert res.status_code == 403
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_Admin['access_token']
    }
    res = client.put(f'/rating/{Rating_C_login.id}', headers=headers, json = reting_without)
    assert res.status_code == 403
    reting_without['user_creator_id'] = login_Admin['new_user_id']


    res = client.put(f'/rating/{Rating_C_login.id}', headers=headers, json = reting_without)
    assert res.status_code == 404
    reting_without['Student_id'] = Student_C.id
    student_without_id['created'] = login_User['new_user_id']
    res = client.put(f'/rating/{Rating_C_login.id}', headers=headers, json=reting_without)
    assert res.status_code == 200
    reting_without['Student_id'] = 0
    reting_without['user_creator_id'] =0
    s.query(Rating).delete()
    s.query(Student).delete()
    s.query(User).delete()


def test_delete_rating(client,login_Admin, login_User, Rating_C_login, Student_C):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']
    }
    res = client.delete('/g/0',headers = headers)
    assert res.status_code == 404
    res = client.delete(f'/g/{Rating_C_login.id}', headers=headers)
    assert res.status_code == 403


    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_Admin['access_token']
    }
    res = client.delete(f'/g/{Rating_C_login.id}', headers=headers)
    assert res.status_code == 200
    s.query(Rating).delete()
    s.query(Student).delete()
    s.query(User).delete()
