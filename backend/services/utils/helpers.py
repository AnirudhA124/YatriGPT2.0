from argon2 import PasswordHasher
import json

ph= PasswordHasher()

HOTELS_DATA=r"C:\Users\Anirudh\Desktop\Python Internship\Project\YatriGPT\backend\data\hotels.json"
HOTEL_BOOKINGS_DATA=r"C:\Users\Anirudh\Desktop\Python Internship\Project\YatriGPT\backend\data\hotel_bookings.json"

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
    
def save_hotels(username:str,hotel_id:int,hotel_name:str,place:str,num_guests:int,guest_names:list,phone_number:str):
    """Add booking details to hotel_bookings.json

    Args:
        username (str): user's username
        hotel_id (int): hotel_id
        hotel_name (str): hotel's name
        place (str): place of visit
        num_guests (int): number of guests
        guest_names (list): names of guests
        phone_number (str): phone number

    Returns:
        bool: True if entered else False
    """
    with open(HOTEL_BOOKINGS_DATA,'r') as f:
        all_bookings=json.load(f)
    if username not in all_bookings:
        all_bookings[username]=[{
            "hotel_id":hotel_id,
            "hotel_name":hotel_name,
            "place":place,
            "num_guests":num_guests,
            "guest_names":guest_names,
            "phone_number":phone_number
        }]
    else:
        list_hotels=all_bookings[username]
        list_hotels.append({
            "hotel_id":hotel_id,
            "hotel_name":hotel_name,
            "place":place,
            "num_guests":num_guests,
            "guest_names":guest_names,
            "phone_number":phone_number
        })
    try:
        with open(HOTEL_BOOKINGS_DATA,'w') as f:
            json.dump(all_bookings,f)
        return True
    except:
        return False
