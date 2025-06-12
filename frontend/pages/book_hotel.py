import os
import sys
import streamlit as st
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.services.utils.helpers import get_hotels
from backend.services.utils.validators import is_valid_phone
from sidebar import render_sidebar

st.markdown("""
<style>
.profile-img {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #f0f0f0;
    margin: 10px auto;
    display: block;
}
.profile-placeholder {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 24px;
    font-weight: bold;
    margin: 10px auto;
}
.centered-header {
    text-align: center;
}
.centered-username {
    text-align: center;
    font-weight: bold;
    font-size: 16px;
    margin-top: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

def book_hotel():
    if "selected_hotel_id" not in st.session_state:
        st.session_state.selected_hotel_id = None
        st.session_state.hotel_id= None
        st.session_state.hotel_name=""
        st.session_state.num_guests=""
        st.session_state.guests_names=[]
        st.session_state.price=None
        st.session_state.check_in=None
        st.session_state.check_out=None

    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    render_sidebar()
    st.title("Hotel Booking")
    if 'username' not in st.session_state:
        st.error("Please log in to book a hotel.")
        return
    username = st.session_state.username
    hotel_data = get_hotels()
    places_name = [place['name'] for place in hotel_data['places']]
    selected_place = st.selectbox("Select a place", places_name)
    number_of_guests=st.selectbox("Number of Guests",[1,2,3,4,5,6,7,8,9,10])
    check_in_date=st.date_input("Check In",value="today")
    check_out_date=st.date_input("Check Out",value="today")
    selected_place_data = None
    for place in hotel_data['places']:
        if place['name'] == selected_place:
            selected_place_data = place
            break

    if selected_place_data:
        # Filter and Sort Controls
        min_price = min(hotel['price'] for hotel in selected_place_data['hotels'])
        max_price = max(hotel['price'] for hotel in selected_place_data['hotels'])
        price_range = st.slider(
            "Price Range",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price)
        )
        sort_by = st.radio(
            "Sort by",
            ["Rating (High to Low)", "Rating (Low to High)", "Price (Low to High)", "Price (High to Low)"]
        )

        # Filter hotels by price
        filtered_hotels = [
            hotel for hotel in selected_place_data['hotels']
            if price_range[0] <= hotel['price'] <= price_range[1]
        ]

        # Sort hotels
        if sort_by == "Rating (High to Low)":
            filtered_hotels.sort(key=lambda x: x['rating'], reverse=True)
        elif sort_by == "Rating (Low to High)":
            filtered_hotels.sort(key=lambda x: x['rating'])
        elif sort_by == "Price (Low to High)":
            filtered_hotels.sort(key=lambda x: x['price'])
        elif sort_by == "Price (High to Low)":
            filtered_hotels.sort(key=lambda x: x['price'], reverse=True)

        st.subheader(f'Hotels in {selected_place}:')
        for hotel in filtered_hotels:
            with st.container(border=True):
                st.subheader(f"{hotel['name']}")
                st.write(f'Price: ₹{hotel['price']}')
                full_stars = int(hotel['rating'])
                stars = "⭐" * full_stars + (5-full_stars)*'☆'
                st.write(f"Rating: {stars} ({hotel['rating']})")
                st.write(f"Amenities: {', '.join(hotel['amenities'])}")

                # Clicking "Book" sets the selected_hotel_id
                if st.button("Book", key=f"book_{hotel['id']}"):
                    st.session_state.selected_hotel_id = hotel['id']

                # Show the form only for the selected hotel
                if st.session_state.selected_hotel_id == hotel['id']:
                    with st.form(key=f"book_{hotel['id']}",enter_to_submit=False):
                        main_guest_name = st.text_input("Name", placeholder="Enter name")
                        # number_of_guests = int(st.number_input("Number of Guests", placeholder="Enter number of guests"))
                        guest_names = [main_guest_name]
                        for i in range(number_of_guests-1):
                            guest_name = st.text_input(
                                f"Guest {i+1} Name",
                                key=f"guest_{i}_{hotel['id']}",
                                placeholder="Enter full name"
                            )
                            guest_names.append(guest_name)
                        phone_number = st.text_input("Phone Number", placeholder="Enter phone number")
                        submit = st.form_submit_button("Submit")
                        if submit:
                            all_names_filled = all(name.strip() for name in guest_names)
                            if main_guest_name and number_of_guests and all_names_filled and phone_number:
                                if is_valid_phone(phone_number):
                                    delta = check_out_date - check_in_date 
                                    st.session_state.hotel_id= hotel['id']
                                    st.session_state.hotel_name=hotel['name']
                                    st.session_state.num_guests=number_of_guests
                                    st.session_state.guest_names=guest_names
                                    st.session_state.price=str(int(hotel['price'])*delta.days)
                                    st.session_state.check_in=check_in_date
                                    st.session_state.check_out=check_out_date
                                    st.success(f"Booked hotel: {hotel['name']}")
                                    st.session_state.selected_hotel_id = None  
                                    with st.spinner("Redirecting to confirm booking page..."):
                                        time.sleep(1)
                                    st.switch_page('pages/confirm_hotel_booking.py')
                                else:
                                    st.error("Enter correct phone number.")
                            else:
                                st.error("Please enter all fields.")
    else:
        st.error("No hotels found for the selected place.")

if __name__=="__main__":
    book_hotel()
