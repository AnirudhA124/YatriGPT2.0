from argon2 import PasswordHasher

ph= PasswordHasher()

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
