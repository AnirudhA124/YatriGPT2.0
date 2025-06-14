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
st.set_page_config(
    page_title="Home",
    initial_sidebar_state="collapsed",
    layout='wide'
)

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


def home_page():
    """Home Page for the web app."""
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
                if card(title="Book Hotels",text="Book Hotels",key="hotels",image=book_hotel()):
                    st.switch_page('pages/book_hotel.py')
                if card(title="Book Train",text="Book Trains",key="train",image=book_train()):
                    st.switch_page('pages/book_train.py')
            with col2:
                if card(title="Itinerary",text="Generate your itinerary",key="itinerary",image=itinerary()):
                    st.switch_page('pages/plan_trips.py')
                if card("Book Flights",text="Book flights",key="flight",image=book_flight()):
                    st.switch_page('pages/book_flight.py')

if __name__ == "__main__":
    home_page()