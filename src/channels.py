from src.data import data
from src.error import InputError, AccessError

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    for users in data['users']:
        if users.get(auth_user_id) == None:
            raise AccessError
    
    return data['channels']

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
