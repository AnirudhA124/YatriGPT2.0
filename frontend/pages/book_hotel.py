import os
import sys
import streamlit as st

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.services.utils.helpers import get_hotels, save_hotels
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
    selected_place_data = None
    for place in hotel_data['places']:
        if place['name'] == selected_place:
            selected_place_data = place
            break

    if selected_place_data:
        st.subheader(f'Hotels in {selected_place}:')
        for hotel in selected_place_data['hotels']:
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
                    with st.form(key=f"book_{hotel['id']}"):
                        main_guest_name = st.text_input("Name", placeholder="Enter name")
                        number_of_guests = int(st.number_input("Number of Guests", placeholder="Enter number of guests"))
                        guest_names = [main_guest_name]
                        for i in range(number_of_guests):
                            guest_name = st.text_input(
                                f"Guest {i+1} Name",
                                key=f"guest_{i}_{hotel['id']}",
                                placeholder="Enter full name"
                            )
                            guest_names.append(guest_name)
                        phone_number = st.text_input("Phone Number", placeholder="Enter phone number")
                        submit = st.form_submit_button("Submit")
                        if submit and main_guest_name and number_of_guests and guest_name and phone_number:
                            if save_hotels(username, hotel['id'], hotel['name'], selected_place, number_of_guests, guest_names, phone_number):
                                st.success(f"Booked hotel: {hotel['name']}")
                                st.session_state.selected_hotel_id = None  # Optionally reset
                            else:
                                st.error(f"Hotel not booked.")
                        else:
                            st.error("Please enter all fields.")
    else:
        st.error("No hotels found for the selected place.")

if __name__=="__main__":
    book_hotel()
