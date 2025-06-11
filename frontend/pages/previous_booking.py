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
from home_page import load_profile_image


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
        
        with st.sidebar:
            st.markdown('<h2 class="centered-header">👤 User Profile</h2>', unsafe_allow_html=True)
            
            # Try to load profile image
            profile_img_data = load_profile_image(username)
            
            if profile_img_data:
                st.markdown(
                    f'<img src="data:image/jpeg;base64,{profile_img_data}" class="profile-img">', 
                    unsafe_allow_html=True
                )
            else:
                # Show placeholder with user's initial
                initial = name[0].upper() if name else 'U'
                st.markdown(
                    f'<div class="profile-placeholder">{initial}</div>', 
                    unsafe_allow_html=True
                )
            
            st.markdown(
                f'<div class="centered-username">@{username}</div>', 
                unsafe_allow_html=True
            )
            prev_bookings=st.button("Previous Bokings",use_container_width=True)
            if prev_bookings:
                pass
            logout=st.button("Logout",use_container_width=True)
            if logout:
                st.session_state.logged_in=False
                st.session_state.username=""
                st.session_state.name=""
                st.switch_page('main.py')
        
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