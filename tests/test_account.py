import pytest
from tests.conftest import client
from tests.test_user import response

@pytest.fixture()
def account_response(client, response):
    access_token = response.json['user']['access']
    response = client.post('/account/create', data={'currency': 840}, headers={'Authorization': f'Bearer {access_token}'})
    return response

def test_create(account_response):
    assert account_response.status_code == 200
    assert account_response.json['message'] == 'Account created successfully'
    assert 'account id' in account_response.json

def test_balance(client, response, account_response):
    access_token = response.json['user']['access']
    account_id = account_response.json['account id']

    response = client.get('/account/balance', data={'id': account_id}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Account balance retrieved successfully'
    assert 'account' in response.json
    assert 'id' in response.json['account']
    assert 'balance' in response.json['account']
    assert 'currency' in response.json['account']
    assert response.json['account']['id'] == account_id
    assert response.json['account']['balance'] == 0
    assert response.json['account']['currency'] == 'USD'

def test_view_transaction_history(client, response, account_response):
    access_token = response.json['user']['access']
    account_id = account_response.json['account id']

    response = client.get('/account/view-transaction-history', data={'id': account_id}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Transaction history retrieved successfully'
    assert 'transactions' in response.json
    assert len(response.json['transactions']) == 0

def test_view_all_transaction_history(client, response, account_response):
    access_token = response.json['user']['access']
    account_id = account_response.json['account id']

    response = client.get('/account/view-all-transaction-history', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'All transaction history retrieved successfully'
    assert 'transactions' in response.json
    assert len(response.json['transactions']) == 0

    client.post('/transaction/deposit', data={'id': account_id, 'amount': 10}, headers={'Authorization': f'Bearer {access_token}'})

    response = client.post('/user/register', data={'username': 'test2', 'email': 'test2@test.com', 'first_name': 'test2', 'last_name': 'test2', 'password': 'test2', 'confirm_password': 'test2'})
    access_token_2 = response.json['user']['access']
    response = client.post('/account/create', data={'currency': 840}, headers={'Authorization': f'Bearer {access_token_2}'})
    account_id_2 = response.json['account id']
    response = client.post('/transaction/transfer', data={'id': account_id, 'receiver_username': 'test2', 'receiver_id': account_id_2, 'amount': 5}, headers={'Authorization': f'Bearer {access_token}'})
    response = client.post('/transaction/withdraw', data={'id': account_id, 'amount': 5}, headers={'Authorization': f'Bearer {access_token}'})

    response = client.get('/account/view-all-transaction-history', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'All transaction history retrieved successfully'
    assert 'transactions' in response.json
    assert len(response.json['transactions']) == 3

def test_delete(client, response, account_response):
    access_token = response.json['user']['access']
    account_id = account_response.json['account id']

    response = client.delete('/account/delete', data={'id': account_id}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Account deleted successfully'

    response = client.get('/account/balance', data={'id': account_id}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404
    assert response.json['error'] == 'Account not found'
