import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

#Need to make a decision about global owners and whether they have access

@pytest.fixture
def create_user1():
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    return auth_register_v1(email,password,firstname, lastname)['auth_user_id']

@pytest.fixture
def create_user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v1(email,password,firstname, lastname)['auth_user_id']

@pytest.fixture
def create_public_channel():
    name = "Testchannel"
    user_id = auth_register_v1("channelcreator@gmail.com", "TestTest", "channelcreator", "last")
    return channels_create_v1(user_id, name, True)['channel_id']

#input errors:
#channel id is not valid
clear_v1()
def test_invalid_channel_id():
    user_id = auth_register_v1("channelcreator2@gmail.com", "TestTest2", "channelcreator2", "last")['auth_user_id']
    channel_id = channels_create_v1(user_id, 'Testchannel', True)
    clear_v1()
    user_id_1 = auth_register_v1("user1@gmail.com", "TestTest2", "user1", "last")['auth_user_id']
    user_id_2 = auth_register_v1("user2@gmail.com", "TestTest2", "user2", "last")['auth_user_id']
    
    with pytest.raises(InputError):
        channel_invite_v1(user_id_1, channel_id, user_id_2)

# u id is not valid
def test_invalid_user_id():
    clear_v1()
    user_id_1 = auth_register_v1("user1@gmail.com", "TestTest2", "user1", "last")['auth_user_id']
    clear_v1()
    auth_user_id = auth_register_v1("channelcreator2@gmail.com", "TestTest2", "channelcreator2", "last")['auth_user_id']
    channel_id = channels_create_v1(user_id, 'Testchannel', True)
    
    with pytest.raises(InputError):
        channel_invite(auth_user_id, channel_id, user_id_1)

#access errors
#auth user not in channel
clear_v1()
def test_unauthorised_user(create_user_1, create_user_2, create_public_channel):
    
    with pytest.raises(AccessError):
        channel_invite_v1(create_user_2, create_public_channel, create_user_1)

clear_v1()
def test_all_valid(create_user_1, create_public_channel):
    auth_user_id = auth_login_v1("channelcreator@gmail.com", "TestTest")['auth_user_id']

    assert channel_invite_v1(auth_user_id, channel_id, user_id_1) == {}