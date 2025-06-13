from argon2 import PasswordHasher
import json

ph= PasswordHasher()

HOTELS_DATA=r"C:\Users\Anirudh\Desktop\Python Internship\Project\YatriGPT\backend\data\hotels.json"
HOTEL_BOOKINGS_DATA=r"C:\Users\Anirudh\Desktop\Python Internship\Project\YatriGPT\backend\data\hotel_bookings.json"
TRAINS_DATA=r"C:\Users\Anirudh\Desktop\Python Internship\Project\YatriGPT\backend\data\trains.json"
TRAIN_BOOKINGS_DATA=r"C:\Users\Anirudh\Desktop\Python Internship\Project\YatriGPT\backend\data\train_bookings.json"
FLIGHTS_DATA=r"C:\Users\Anirudh\Desktop\Python Internship\Project\YatriGPT\backend\data\flights.json"
FLIGHTS_BOOKING_DATA=r"C:\Users\Anirudh\Desktop\Python Internship\Project\YatriGPT\backend\data\flight_bookings.json"

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
    
def save_hotels(username:str,hotel_id:int,hotel_name:str,place:str,num_guests:int,guest_names:list,phone_number:str,price:str,check_in_date,check_out_date):
    """Add Bookings to hotel_booking.json.

    Args:
        username (str): User's username.
        hotel_id (int): Hotel Id for booked hotel.
        hotel_name (str): Hotel Name.
        place (str): place of visit.
        num_guests (int): Number of guests.
        guest_names (list): guests names.
        phone_number (str): user's phone number.
        price (str): price of hotel.
        check_in_date (Date): check in date.
        check_out_date (Date): check out date.

    Returns:
        bool: True if booked else False.
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
            "phone_number":phone_number,
            "price":price,
            "check_in_date":check_in_date,
            "check_out_date":check_out_date
        }]
    elif username in all_bookings:
        list_hotels=all_bookings[username]
        list_hotels.append({
            "hotel_id":hotel_id,
            "hotel_name":hotel_name,
            "place":place,
            "num_guests":num_guests,
            "guest_names":guest_names,
            "phone_number":phone_number,
            "price":price,
            "check_in_date":check_in_date,
            "check_out_date":check_out_date
        })
    try:
        with open(HOTEL_BOOKINGS_DATA,'w') as f:
            json.dump(all_bookings,f)
        return True
    except:
        return False

def get_hotel_booking():
    """Returns previous booking data for hotels.

    Returns:
        json: Hotel booking history.
    """
    with open(HOTEL_BOOKINGS_DATA,'r') as f:
        return json.load(f)


def get_trains():
    """Returns train data.

    Returns:
        json: returns json data for trains.
    """
    with open(TRAINS_DATA,'r') as f:
        return json.load(f)

def save_train_data(data):
    """Save train data.

    Args:
        data (json): data to be saved.
    """
    with open(TRAINS_DATA,'w') as f:
        json.dump(data,f)
    
def book_train(num_seats: int, train_num: str, tier: str):
    """Book train with train number number of seats and tier.

    Args:
        num_seats (int): number of seats to book.
        train_num (str): train number.
        tier (str): tier ie AC3, AC2,etc.

    Returns:
        bool: Total fare if booked else False.
    """
    all_trains = get_trains()
    
    for train in all_trains['trains']:
        if train['train_number'] == train_num:
            for cls in train['classes']:
                if cls['name'] == tier:  # Fixed comparison
                    if cls['available'] >= num_seats:  # Fixed condition
                        cls['available'] -= num_seats
                        save_train_data(all_trains)
                        return True
                    else:
                        return False
            # Class not found in train
            return False
    # Train not found
    return False

def save_train_booking(username:str,train_name:str,train_number:str,number_of_guests:int,price:int,tier:str,travel_date):
    """Saving train bookings.

    Args:
        username (str): user's username
        train_name (str): train name
        train_number (str): train number
        number_of_guests (int): number of seats booked
        price (int): price
        tier (str): tier (AC2,AC3,etc)
        travel_date (_type_): date of journey

    Returns:
        bool: True if booked else False.
    """
    with open(TRAIN_BOOKINGS_DATA,'r') as f:
        all_bookings=json.load(f)
    if username not in all_bookings:
        all_bookings[username]=[{
            "train_name":train_name,
            "train_number":train_number,
            "number_of_seats":number_of_guests,
            "tier":tier,
            "travel_date":travel_date,
            "price":price
        }]
    elif username in all_bookings:
        list_trains=all_bookings[username]
        list_trains.append({
            "train_name":train_name,
            "train_number":train_number,
            "number_of_seats":number_of_guests,
            "tier":tier,
            "travel_date":travel_date,
            "price":price
        })
    try:
        with open(TRAIN_BOOKINGS_DATA,'w') as f:
            json.dump(all_bookings,f)
        return True
    except:
        return False

def get_train_bookings():
    """Returns train bookings.

    Returns:
        json: returns train bookings
    """
    with open(TRAIN_BOOKINGS_DATA,'r') as f:
        return json.load(f)

def get_flights():
    """Returns flight data.

    Returns:
        json: returns flight data.
    """
    with open(FLIGHTS_DATA,'r') as f:
        return json.load(f)

def book_flight(username:str,airline:str,source:str,destination:str,num_guests:int,price:str,travel_date):
    """Books flight and add data in flught_bookings.json

    Args:
        username (str): user's username.
        airline (str): airlines by which user will travel.
        source (str): source.
        destination (str): destination.
        num_guests (int): number of passengers along with user.
        price (str): total price of tickets.
        travel_date (_type_): travel date.

    Returns:
        bool: True if booked else false.
    """
    with open(FLIGHTS_BOOKING_DATA,'r') as f:
        all_bookings=json.load(f)
    if username not in all_bookings:
        all_bookings[username]=[{
            "airline":airline,
            "from":source,
            "to":destination,
            "number_of_guests":num_guests,
            "price":price,
            "travel_date":travel_date
        }]
    elif username in all_bookings:
        list_flights=all_bookings[username]
        list_flights.append({
            "airline":airline,
            "from":source,
            "to":destination,
            "number_of_guests":num_guests,
            "price":price,
            "travel_date":travel_date
        })
    try:
        with open(FLIGHTS_BOOKING_DATA,'w') as f:
            json.dump(all_bookings,f)
        return True
    except:
        return False

def get_flight_bookings():
    """Returns flight booking data.

    Returns:
        json: fliht booking data is retuened
    """
    with open(FLIGHTS_BOOKING_DATA,'r') as f:
        return json.load(f)