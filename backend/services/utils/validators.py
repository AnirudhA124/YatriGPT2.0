import re
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)


def contains_special_char(s):
    return bool(re.search(r'[^a-zA-Z0-9]', s))


def is_valid_email(email:str):
    """Check email's validity that email contains @ and .
        or not.

    Args:
        email (str): users's email

    Returns:
        bool: True if valid else False
    """
    if '@' in email and '.' in email:
        return True
    else:
        return False

def is_valid_phone(phone_number:str):
    """Checks validity of phone number that is the length 
        more than 10 or not.

    Args:
        phone_number (str): user's phone number

    Returns:
        bool: True if valid else False
    """
    if len(phone_number)==10 and phone_number.isdigit():
        return True
    else:
        False

def is_valid_password(password:str):
    """Checks validity of password that is the password contains 
        special character or not and if length of password is more than 
        8 or not.

    Args:
        password (str): password entered by user

    Returns:
        bool: True if valid else False
    """
    if contains_special_char(password) and len(password)>=8:
        return True
    else:
        return False

def is_username_exits(username:str):
    """Checks if username exists

    Args:
        username (str): users's username

    Returns:
        bool: True if username exits False if not
    """
    from auth.auth_utils import load_users
    all_users=load_users()
    if username in all_users:
        return True
    else:
        return False 
