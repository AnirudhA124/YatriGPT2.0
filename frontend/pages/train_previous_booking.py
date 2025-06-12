import streamlit as st
import os
import sys
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)
from sidebar import render_sidebar
from backend.services.utils.helpers import get_train_bookings


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

def previous_train_booking():
    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    else:
        render_sidebar()
        username=st.session_state.username
        all_train_booking=get_train_bookings()
        for user in all_train_booking:
            if user==username:
                train_bookings=all_train_booking[user]
                for booking in train_bookings:
                    with st.container(border=True):
                        st.header(f"{booking['train_name']} ({booking['train_number']})")
                        st.markdown(f"**Train Name:** {booking['train_name']}")
                        st.markdown(f"**Number of Seats:** {booking['number_of_seats']}")
                        st.markdown(f"**Tier:** {booking['tier']}")
                        st.markdown(f"**Travel Date:** {booking['travel_date']}")
                        st.markdown(f"**Price:** {booking['price']}")
        if username not in all_train_booking:
            st.title("No Bookings Yet!")
        

if __name__=="__main__":
    previous_train_booking()
