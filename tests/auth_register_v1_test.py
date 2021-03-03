import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1 
from src.error import InputError 

# Test exception - Email entered is not valid (wrong format)
def test_given_email_is_invalid():
    clear_v1() 

    with pytest.raises(InputError):
        auth_register_v1('@unsw.edu.au', 'password', 'first1', 'last1')
    
    with pytest.raises(InputError):
        auth_register_v1('test.unsw.edu.au', 'password', 'first2', 'last2')

    with pytest.raises(InputError):
        auth_register_v1('test@.au', 'password', 'first3', 'last3')
    
    with pytest.raises(InputError):
        auth_register_v1('test_special!!!@unsw.edu.au', 'password', 'firstspecial', 'lastspecial')

# Test exception - Email entered already exists (belongs to an existing user)
def test_email_already_exists():
    clear_v1()

    auth_register_v1('testing123@unsw.edu.au', 'password', 'first123', 'last123')
    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.edu.au', 'hello123', 'first1', 'last1')
    
    auth_register_v1('testing567@unsw.edu.au', 'password', 'first567', 'last567')
    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.edu.au', 'hello567', 'first2', 'last2')
    
    auth_register_v1('testing890@unsw.edu.au', 'password', 'first890', 'last890')
    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.edu.au', 'hello890', 'first3', 'last3')

# Test exception - Password given is less than 6 Characters
def test_password_incorrect_length():
    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.edu.au', '', 'first1', 'last1')  

    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.edu.au', '2', 'first2', 'last2') 
    
    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.edu.au', '@3456', 'first3', 'last3') 

# Test exception - First name given is between 1 and 50 inclusive 
def test_first_name_valid_length():
    clear_v1() 

    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.edu.au', 'password', '', 'last1') 
    
    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.edu.au', 'password', 'thisfirstnameismorethanfiftycharacterslong123123123123123', 'last2')
    
    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.edu.au', 'password', 'thisfirstnamecontainsspecialcharacters##^^&&**!!123123123', 'last3')   

# Test exception - Last name given is between 1 and 50 inclusive 
def test_last_name_valid_length():
    clear_v1()
    
    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.edu.au', 'password', 'first1', '')
    
    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.edu.au', 'password', 'first2', 'thislastnameismorethanfiftycharacterslong123123123123123') 
    
    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.edu.au', 'password', 'first3', 'thislastnamecontainsspecialcharacters##^^&&**!!123123123')

# Test registration of details was successful - if registration is successful then you can login 
def test_registration_successful():
    clear_v1()

    userid_1 = auth_register_v1('testing123@unsw.edu.au', 'password', 'first1', 'last1') 
    userid_2 = auth_register_v1('testing567@unsw.edu.au', 'password', 'first2', 'last2') 
    userid_3 = auth_register_v1('testing890@unsw.edu.au', 'password', 'first3', 'last3') 

    assert auth_login_v1('testing123@unsw.edu.au', 'password') == userid_1
    assert auth_login_v1('testing567@unsw.edu.au', 'password') == userid_2
    assert auth_login_v1('testing890@unsw.edu.au', 'password') == userid_3 


# Tests for handle - no @ or whitespace, 20 characters only, Q - in the case where we need to add numbers to handles as the handle already exists, is it allowed to go over the 20 character limiit?
# Need clarification on names and handles - are @ and whitespace allowed in names?
# Assume can have same name but different emails, numbers and special characters allowed in names 