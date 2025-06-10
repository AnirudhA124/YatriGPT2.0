import json
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.helpers import hash_password, verify_password

USERS_FILE = r"C:\Users\Anirudh\Desktop\Python Internship\Project\YatriGPT\backend\data\users.json"

def load_users():
    """Load users from json file.

    Returns:
        json_string: users data in json format
    """
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Save users data.

    Args:
        users (object): json object
    """
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def add_user(name: str, username: str, password: str, email: str, phone_number: str, preferences: list):
    """Adds user in users.json if username not exists.

    Args:
        name (str): User's name
        username (str): User's username
        password (str): User's password
        email (str): User's email
        phone_number (str): User's phone number
        preferences (list): User's preferences

    Returns:
        bool: Returns True if user added else False if not added(ie Users exists).
    """
    all_user = load_users()
    if username not in all_user:
        all_user[username] = {
            "name": name,
            "password": hash_password(password),
            "email": email,
            "phone_number": phone_number,
            "preferences": preferences
        }
        save_users(all_user)
        return True
    else:
        return False

def verify_user(username: str, password: str):
    """Verify user based on his credentials

    Args:
        username (str): username entered by user
        password (str): password entered by user

    Returns:
        bool: True if valid else False
    """
    all_users = load_users()
    try:
        if username in all_users:
            return verify_password(all_users[username]['password'], password)
        return False
    except Exception as e:
        return False
