from tests.conftest import *
#from  pytest_mock  import *
def test_add_user(client):

    res = client.post('/register', json=user_admin)
    assert any(res.get_json()['access_token'])
    res = client.post('/register', json=wrong_user)
    assert res.get_json() == {"message": "You should set a correct property."}
    res = client.post('/register', json=Abslut_wrong_user)
    assert res.status_code == 422
    res = client.post('/register', json=user_admin)
    assert res.get_json() == {"message": "User with this username already exists."}
    #print(res.get_json())

def test_login(client, user_C):
    res = client.post('/login', json={"username":"wrong", "password" : "1"})
    assert res.status_code == 404
    res = client.post('/login', json={"username":user_C.username, "password" : "-1"})
    assert res.status_code == 406
    res = client.post('/login', json={"username":user_C.username, "password" : "1"})
    assert res.get_json()['access_token'] != ""
    s.query(User).delete()

def test_get_user(client, login_User, user_C):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']

    }
    #{"username": "username1", "password": "1"}
    res = client.get('/user/0',headers = headers)
    assert res.status_code == 404
    #see anther user
    user_id = login_User['new_user_id']
    res = client.get(f'/user/{user_C.id}', headers=headers)
    assert res.status_code == 403
    res = client.get(f'/user/{user_id}', headers=headers)
    assert res.status_code == 200

def test_put_user(client, login_User, user_C):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']

    }
    #{"username": "username1", "password": "1"}
    res = client.put('/user/0',headers = headers, json = user_without_id)
    assert res.status_code == 400
    #put anther user
    user_id = login_User['new_user_id']
    res = client.put(f'/user/{user_id}', headers=headers)
    assert res.status_code == 400
    res = client.put(f'/user/{user_id}', headers=headers, json=user_user)
    assert res.status_code == 400
    res = client.put(f'/user/{user_C.id}', headers=headers, json={"username": login_User['new_user_username']})
    assert res.status_code == 403
    res = client.put(f'/user/{user_id}', headers=headers, json={"username": login_User['new_user_username']})
    assert res.status_code == 406
    res = client.put(f'/user/{user_id}', headers=headers, json=user_without_id)
    assert res.status_code == 200

def test_logout(client, login_User):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']

    }
    # {"username": "username1", "password": "1"}
    user_id = login_User['new_user_id']
    res = client.delete('/logout', headers=headers)
    assert res.status_code == 200


def test_delet_user(client, login_User, user_C):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + login_User['access_token']

    }
    #{"username": "username1", "password": "1"}
    res = client.delete('/user/0',headers = headers)
    assert res.status_code == 404
    #see anther user
    user_id = login_User['new_user_id']
    res = client.delete(f'/user/{user_C.id}', headers=headers)
    assert res.status_code == 403
    res = client.delete(f'/user/{user_id}', headers=headers)
    assert res.status_code == 200
