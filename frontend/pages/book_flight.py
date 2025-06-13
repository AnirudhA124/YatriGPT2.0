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
        st.error("Please log in to book a flight.")  # Note: Should say "train" if booking trains
        return

    username = st.session_state.username
    places = ["Goa", "Shimla", "Jaipur", "Darjeeling", "Kerela", "Delhi", "Indore"]
    source = st.selectbox("Source", places)
    destination = st.selectbox("Destination", [place for place in places if place != source])
    number_of_seats=st.selectbox("Number of Seats",[1,2,3,4,5])
    travel_date=st.date_input("Travel Date",value="today")
    # Fetch train data
    flight_data = get_flights()

    # Filter trains by source and destination
    filtered_flight=[flight for flight in flight_data if flight["from"]==source and flight["to"]==destination and datetime.datetime.fromisoformat(flight['departure']).date()==travel_date]
    

    # Display each train in a container with availability and prices
    for flight in filtered_flight:
        with st.container(border=True):
            st.header(flight['airline'])
            st.markdown(f'**From:** {flight['from']}')
            st.markdown(f'**To:** {flight['to']}')
            st.markdown(f'**Departure:** {flight['departure']}')
            st.markdown(f'**Fare:** {flight['fare']}')

            if st.button("Book Now", key=f"book_{flight['flight_id']}"):
                st.session_state.flight_airline=flight['airline']
                st.session_state.source=flight['from']
                st.session_state.destination=flight['to']
                st.session_state.number_of_seats=number_of_seats
                st.session_state.travel_date=travel_date
                st.session_state.price=flight['fare']*number_of_seats
                st.switch_page('pages/confirm_flight_booking.py')
                


if __name__ == "__main__":
    book_flight()
