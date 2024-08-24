import pytest
from tests.conftest import client

def token():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    return token


def test_register(client):
    response = client.post('/user/register', data={'username': 'test', 'email': 'test@test.test', 'first_name': 'test', 'last_name': 'test', 'password': 'test', 'confirm_password': 'test'})
    assert response.status_code == 200
    assert response.json['message'] == 'User registered successfully'
    assert 'access' in response.json['user']
    assert 'refresh' in response.json['user']

    response = client.post('/user/register', data={'username': 'test', 'email': 'test@test.test', 'first_name': 'test', 'last_name': 'test', 'password': 'test', 'confirm_password': 'test'})
    assert response.status_code == 402
    assert response.json['error'] == 'Username or email already exists'

@pytest.fixture()
def response(client):
    client.post('/user/register', data={'username': 'test', 'email': 'test@test.test', 'first_name': 'test', 'last_name': 'test', 'password': 'test', 'confirm_password': 'test'})
    response = client.post('/user/login', data={'username': 'test', 'password': 'test'})    
    return response

def test_login(response):
    assert response.status_code == 200
    assert response.json['message'] == 'User logged in successfully'
    assert 'access' in response.json['user']
    assert 'refresh' in response.json['user']

def test_invalid_login(client, response):
    response = client.post('/user/login', data={'username': 'test1', 'password': 'test1'})

    assert response.status_code == 404
    assert response.json['error'] == 'User not found'

    response = client.post('/user/login', data={'username': 'test', 'password': 'test1'})

    assert response.status_code == 402
    assert response.json['error'] == 'Invalid username or password'

def test_view_profile(client, response):
    access_token = response.json['user']['access']

    response = client.get('/user/view-profile', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'User retreived successfully'
    assert response.json['user']['username'] == 'test'
    assert response.json['user']['email'] == 'test@test.test'
    assert response.json['user']['first name'] == 'test'
    assert response.json['user']['last name'] == 'test'

def test_update(client, response):
    access_token = response.json['user']['access']

    response = client.put('/user/update', data={'first_name': 'test2', 'last_name': 'test2', 'new_password': 'test2', 'confirm_new_password': 'test2'}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'User information updated successfully'

    response = client.get('/user/view-profile', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['user']['first name'] == 'test2'
    assert response.json['user']['last name'] == 'test2'

def test_token_management(client):
    response = client.get('/user/view-profile')

    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'
    
    response = client.get('/user/view-profile', headers={'Authorization': f'Bearer {token()}'})
    assert response.status_code == 422
    assert response.json['msg'] == 'Signature verification failed'

def test_logout(client, response):
    access_token = response.json['user']['access']

    response = client.delete('/user/logout', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'User logged out successfully'

    response = client.get('/user/view-profile', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 401
    assert response.json['msg'] == 'Token has been revoked'

def test_logout_refresh(client, response):
    refresh_token = response.json['user']['refresh']

    response = client.delete('/user/logout-refresh', headers={'Authorization': f'Bearer {refresh_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'User logged out successfully'

def test_delete(client, response):
    access_token = response.json['user']['access']
    
    response = client.delete('/user/delete', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'User deleted successfully'

    response = client.post('/user/login', data={'username': 'test', 'password': 'test'})
    assert response.status_code == 404
    assert response.json['error'] == 'User not found'

def test_delete_with_accounts(client, response):
    access_token = response.json['user']['access']
    
    response = client.post('/account/create', data={'currency': 840}, headers={'Authorization': f'Bearer {access_token}'})
    account_id = response.json['account id']
    client.post('/transaction/deposit', data={'id': account_id, 'amount': 100}, headers={'Authorization': f'Bearer {access_token}'})

    response = client.delete('/user/delete', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 402
    assert response.json['error'] == 'Please withdraw all funds before deleting account'

def test_view_accounts(client, response):
    access_token = response.json['user']['access']
    
    response = client.get('/user/view-accounts', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'No accounts found'

def test_refresh(client, response):
    refresh_token = response.json['user']['refresh']

    response = client.post('/user/refresh', headers={'Authorization': f'Bearer {refresh_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Token refreshed successfully'
    assert 'access' in response.json['user']
    assert 'refresh' in response.json['user']
