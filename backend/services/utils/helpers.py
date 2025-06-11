from argon2 import PasswordHasher
import json

ph= PasswordHasher()

HOTELS_DATA=r"C:\Users\Anirudh\Desktop\Python Internship\Project\YatriGPT\backend\data\hotels.json"

def hash_password(password:str):
    """To hash password.

    Args:
        password (str): password entered by user.

    Returns:
        str: hashed password
    """
    hash=ph.hash(password)
    return hash

def verify_password(password_hash:str,password:str):
    """To verify password.

    Args:
        password_hash (str): hashed password stored in database.
        password (str): password entered by user (to be verified).

    Returns:
        bool: True if verified else False.
    """
    return ph.verify(password_hash,password)

def get_hotels():
    """Returns hotel data.

    Returns:
        json: hotel data is being returned.
    """
    with open(HOTELS_DATA,'r') as f:
        return json.load(f)
