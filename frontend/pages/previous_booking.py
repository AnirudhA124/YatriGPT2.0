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
        st.title(f"Welcome {name}")

        # Show spinner while loading cards
        with st.spinner('Loading booking options...'):            
            col1,col2=st.columns(2)

            with col1:
                if card(title="Hotels Bookings",text="View yor Hotel Bookings Here",key="hotels",image=book_hotel()):
                    pass
                if card(title="Train Bookings",text="View yor Train Bookings Here",key="train",image=book_train()):
                    pass
            with col2:
                if card(title="Activities Bookings",text="View yor Activities Bookings Here",key="activities",image=activities()):
                    pass
                if card("Flights Bookings",text="View yor Flight Bookings Here",key="flight",image=book_flight()):
                    pass

if __name__ == "__main__":
    previous_bookings()