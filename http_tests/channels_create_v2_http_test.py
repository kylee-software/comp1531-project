import pytest
import requests
from src import config
from src.helper import create_token

def clear():
    '''
    Reset the data
    '''
    empty_data = requests.delete(config.url + 'clear/v1').json()
    return

@pytest.fixture
def token():
    '''
    create a token
    '''
    clear()
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstname"
    last_name = "lastname"
    auth_resp = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    })
    token = auth_resp.json()['token']
    return token

def test_invalid_name(token):
    '''
    Test for invalid channel name when it's empty or more than 20 characters

    Status code for InputError is 400
    '''
    resp1 = requests.post(config.url + 'channels/create/v2', json={
        'token': token,
        'name': "",
        'is_public': True
    })

    resp2 = empty_resp = requests.post(config.url + 'channels/create/v2', json={
        'token': token,
        'name': "fffffffffffffffffffff",
        'is_public': True
    })

    # Getting status code the InputError
    status_code1 = resp1.status_code
    status_code2 = resp2.status_code

    assert status_code1 == 400
    assert status_code2 == 400

def test_invalid_token():
    '''
        Test for invalid token

        Status code for AccessError is 403
    '''
    clear()
    token = create_token(5, 1)
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': token,
        'name': "channelName1",
        'is_public': True
    })

    status_code = resp.status_code
    assert status_code == 403

def test_valid_channel_id(token):
    channel_resp = requests.post(config.url + 'channels/create/v2', json={
        'token': token,
        'name': "channelName1",
        'is_public': True
    })

    channel_id = channel_resp.json()['channel_id']
    assert channel_id == 1
