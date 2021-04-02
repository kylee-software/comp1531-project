import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1
from src.error import InputError 

# Test exception - Email given is not valid (wrong format)
def test_invalid_email(): 
    clear_v1() 

    invalid_email_1 = '@unsw.edu.au'
    with pytest.raises(InputError): 
        auth_login_v1(invalid_email_1, 'password')
    
    invalid_email_2 = 'test@.au'
    with pytest.raises(InputError):
        auth_login_v1(invalid_email_2, 'password') 
    
    invalid_email_3 = 'test.unsw.edu.au'
    with pytest.raises(InputError):
        auth_login_v1(invalid_email_3, 'password')
    
    invalid_email_4 = 'test_special!!!@unsw.au'
    with pytest.raises(InputError):
        auth_login_v1(invalid_email_4, 'password') 

    clear_v1() 

# Test exception - Email given does not match a user's email (email doesn't exist)
def test_email_nonexistent():
    clear_v1()

    auth_register_v1('testing123@unsw.au', 'password', 'first123', 'last123') 
    with pytest.raises(InputError):
        auth_login_v1('testfail1@unsw.au', 'password')
    
    auth_register_v1('testing567@unsw.au', 'password', 'first567', 'last567') 
    with pytest.raises(InputError):
        auth_login_v1('testfail2@unsw.au', 'password') 

    auth_register_v1('testing890@unsw.au', 'password', 'first890', 'last890') 
    with pytest.raises(InputError):
        auth_login_v1('testfail3@unsw.au', 'password') 
    
    clear_v1()

# Test exception - password given is not correct  
def test_password_incorrect():
    clear_v1()

    auth_register_v1('testing123@unsw.au', 'password', 'first123', 'last123') 
    with pytest.raises(InputError):
        auth_login_v1('testing123@unsw.au', 'failed123')
    
    auth_register_v1('testing567@unsw.au', 'password', 'first567', 'last567') 
    with pytest.raises(InputError):
        auth_login_v1('testing567@unsw.au', 'failed567')
    
    auth_register_v1('testing890@unsw.au', 'password', 'first890', 'last890') 
    with pytest.raises(InputError):
        auth_login_v1('testing890@unsw.au', 'failed890')
    
    clear_v1()

# Test - email and password given are correct
def test_correct_login_details():
    clear_v1()

    userid_1 = auth_register_v1('testing123@unsw.au', 'password', 'first123', 'last123') 
    userid_2 = auth_register_v1('testing567@unsw.au', 'password', 'first567', 'last567') 
    userid_3 = auth_register_v1('testing890@unsw.au', 'password', 'first890', 'last890') 

    assert auth_login_v1('testing123@unsw.au', 'password') == userid_1  
    assert auth_login_v1('testing567@unsw.au', 'password') == userid_2 
    assert auth_login_v1('testing890@unsw.au', 'password') == userid_3   

    clear_v1()
