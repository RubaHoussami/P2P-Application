from tests.conftest import client
from tests.test_user import response
from tests.test_account import account_response

def test_transfer(client, response, account_response):
    access_token = response.json['user']['access']
    account_id = account_response.json['account id']
    client.post('/transaction/deposit', data={'id': f'{account_id}', 'amount': 10}, headers={'Authorization': f'Bearer {access_token}'})

    response = client.post('/transaction/transfer', data={'id': account_id, 'receiver_username': 'test', 'receiver_id': account_id, 'amount': 5}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 402
    assert response.json['error'] == 'Cannot transfer to self'

    response = client.post('/user/register', data={'username': 'test2', 'email': 'test2@test.com', 'first_name': 'test2', 'last_name': 'test2', 'password': 'test2', 'confirm_password': 'test2'})
    access_token_2 = response.json['user']['access']
    response = client.post('/account/create', data={'currency': 840}, headers={'Authorization': f'Bearer {access_token_2}'})
    account_id_2 = response.json['account id']

    response = client.post('/transaction/transfer', data={'id': account_id, 'receiver_username': 'test2', 'receiver_id': account_id_2, 'amount': 5}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Transfer successful'

    response = client.post('/transaction/transfer', data={'id': account_id, 'receiver_username': 'test2', 'receiver_id': account_id_2, 'amount': 100}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 402
    assert response.json['error'] == 'Insufficient funds'
    
    response = client.post('/account/create', data={'currency': 422}, headers={'Authorization': f'Bearer {access_token_2}'})
    account_id_3 = response.json['account id']

    response = client.post('/transaction/transfer', data={'id': account_id, 'receiver_username': 'test2', 'receiver_id': account_id_3, 'amount': 5}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 402
    assert response.json['error'] == 'Currency mismatch'

    response = client.post('/transaction/transfer', data={'id': account_id, 'receiver_username': 'test2', 'receiver_id': 10, 'amount': 5}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404
    assert response.json['error'] == 'Receiver account not found'



def test_deposit(client, response, account_response):
    access_token = response.json['user']['access']
    account_id = account_response.json['account id']
    response = client.post('/transaction/deposit', data={'id': f'{account_id}', 'amount': 5}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200
    assert response.json['message'] == 'Deposit successful'

def test_withdraw(client, response, account_response):
    access_token = response.json['user']['access']
    account_id = account_response.json['account id']
    response = client.post('/transaction/withdraw', data={'id': f'{account_id}', 'amount': 5}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 402
    assert response.json['error'] == 'Insufficient funds'

    client.post('/transaction/deposit', data={'id': f'{account_id}', 'amount': 5}, headers={'Authorization': f'Bearer {access_token}'})
    response = client.post('/transaction/withdraw', data={'id': f'{account_id}', 'amount': 5}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200
    assert response.json['message'] == 'Withdrawal successful'
