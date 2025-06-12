import streamlit as st
import os
import sys
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)
from sidebar import render_sidebar
from backend.services.utils.helpers import get_hotel_booking


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

def previous_hotel_booking():
    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    else:
        render_sidebar()
        username=st.session_state.username
        all_hotel_booking=get_hotel_booking()
        for user in all_hotel_booking:
            if user==username:
                hotels=all_hotel_booking[user]
                for hotel in hotels:
                    with st.container(border=True):
                        st.subheader(f"{hotel['hotel_name']}")
                        st.write(f'Number of guests:{hotel['num_guests']}')
                        st.write(f"Names of guests:")
                        for i in hotel['guest_names']:
                            st.markdown(f' - {i}')
                        st.write(f'Place:{hotel['place']}')
                        st.write(f'Check In Date:{hotel['check_in_date']}')
                        st.write(f'Check Out Date:{hotel['check_out_date']}')
                        st.write(f'Price: ₹{hotel['price']}')
        if username not in all_hotel_booking:
            st.title("No Bookings Yet!")

if __name__=="__main__":
    previous_hotel_booking()
