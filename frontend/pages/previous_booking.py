import streamlit as st
import base64
import os
import time
from pathlib import Path
from streamlit_card import card
from backend.constants.background_imges import (cover_image,book_hotel,book_flight,book_train,
                                                restaurants,itinerary,activities)
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)
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


def previous_bookings():
    """Previous bookings page for the web app."""
    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    else:
        name = st.session_state.get('name', 'User')
        username = st.session_state.get('username', 'user')
        
        render_sidebar()
        
        custom_html = cover_image()
        # Display the custom HTML
        st.markdown(
                custom_html, 
                unsafe_allow_html=True
            )
        st.title(f"Booking History")

        # Show spinner while loading cards
        with st.spinner('Loading booking options...'):            
            col1,col2=st.columns(2)

            with col1:
                if card(title="Hotels Bookings",text="View your Hotel Bookings Here",key="hotels",image=book_hotel()):
                    st.switch_page('pages/hotel_previous_bookings.py')
                if card(title="Train Bookings",text="View your Train Bookings Here",key="train",image=book_train()):
                    st.switch_page('pages/train_previous_booking.py')
            with col2:
                if card(title="Plans",text="View your Plans Here",key="plans",image=activities()):
                    st.switch_page('pages/trip_history.py')
                if card("Flights Bookings",text="View your Flight Bookings Here",key="flight",image=book_flight()):
                    st.switch_page('pages/flight_previous_booking.py')

if __name__ == "__main__":
    previous_bookings()