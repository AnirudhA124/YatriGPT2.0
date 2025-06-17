import os
import sys
import streamlit as st
from backend.services.utils.helpers import get_flights
from backend.services.utils.validators import is_valid_phone
from sidebar import render_sidebar
import datetime

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

def book_flight():
    if "selected_flight_id" not in st.session_state:
        st.session_state.selected_flight_id = None

    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    render_sidebar()
    st.title("Flight Booking")
    if 'username' not in st.session_state:
        st.error("Please log in to book a flight.")
        return

    username = st.session_state.username
    places = ["Goa", "Shimla", "Jaipur", "Darjeeling", "Kerela", "Delhi", "Indore"]
    source = st.selectbox("Source", places)
    destination = st.selectbox("Destination", [place for place in places if place != source])
    number_of_seats = st.selectbox("Number of Seats", [1, 2, 3, 4, 5])
    travel_date = st.date_input("Travel Date", value="today", min_value="today")
    # Get flight data
    flight_data = get_flights()

    # Filter flights by source, destination, and date
    filtered_flight = [
        flight for flight in flight_data 
        if (
            flight["from"] == source 
            and flight["to"] == destination 
            and datetime.datetime.fromisoformat(flight['departure']).date() == travel_date
        )
    ]

    # Add airline filter
    airlines = list({flight['airline'] for flight in filtered_flight})
    airlines.insert(0, "All")
    selected_airline = st.selectbox("Filter by Airline", airlines)

    # Filter by airline if not "All"
    filtered_flight = [
        flight for flight in filtered_flight 
        if (selected_airline == "All" or flight['airline'] == selected_airline)
    ]

    # Add sort order selector
    sort_order = st.radio(
        "Sort by fare:",
        ["Lowest to Highest", "Highest to Lowest"],
        horizontal=True
    )

    # Sort flights
    if sort_order == "Lowest to Highest":
        filtered_flight = sorted(filtered_flight, key=lambda x: x['fare'])
    else:
        filtered_flight = sorted(filtered_flight, key=lambda x: x['fare'], reverse=True)

    # Display each flight
    for flight in filtered_flight:
        with st.container(border=True):
            st.header(flight['airline'])
            st.markdown(f'**From:** {flight["from"]}')
            st.markdown(f'**To:** {flight["to"]}')
            st.markdown(f'**Departure:** {flight["departure"]}')
            st.markdown(f'**Fare:** {flight["fare"]}')

            if st.button("Book Now", key=f"book_{flight['flight_id']}"):
                st.session_state.selected_flight_id = flight['flight_id']

            if st.session_state.selected_flight_id == flight['flight_id']:
                with st.form(key=f"book_{flight['flight_id']}", clear_on_submit=False):
                    # Main passenger
                    name = st.text_input("Name", placeholder="Enter your name", key=f"main_{flight['flight_id']}")
                    guests_names = [name] if name else []
                    # Additional guests (number_of_seats - 1)
                    for i in range(1, number_of_seats):
                        guest_name = st.text_input(
                            f"Guest {i} Name",
                            key=f"guest_{i}_{flight['flight_id']}",
                            placeholder="Enter guest name"
                        )
                        guests_names.append(guest_name)
                    phone_number = st.text_input("Phone Number", key=f"phone_{flight['flight_id']}", placeholder="Enter phone number")
                    submit = st.form_submit_button("Submit")
                    if submit:
                        all_names_filled = all(name.strip() for name in guests_names) if guests_names else False
                        if all_names_filled and phone_number:
                            if is_valid_phone(phone_number):
                                st.session_state.guests_names = guests_names
                                st.session_state.flight_airline = flight['airline']
                                st.session_state.source = flight['from']
                                st.session_state.destination = flight['to']
                                st.session_state.number_of_seats = number_of_seats
                                st.session_state.travel_date = travel_date
                                st.session_state.price = flight['fare'] * number_of_seats
                                st.switch_page('pages/confirm_flight_booking.py')
                            else:
                                st.error("Please enter a valid phone number.")
                        else:
                            st.error("Please fill in all names and phone number.")

if __name__ == "__main__":
    book_flight()
