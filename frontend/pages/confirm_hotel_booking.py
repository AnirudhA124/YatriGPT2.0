import streamlit as st
import os
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

def confirm_hotel_booking():
    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    else:
        render_sidebar()
        st.title("Confirm Booking!")
        hotel_id=st.session_state.hotel_id    
        hotel_name=st.session_state.hotel_name
        number_of_guests=st.session_state.num_guests
        guests_names=st.session_state.guest_names
        price=st.session_state.price
        check_in_date=st.session_state.check_in
        check_out_date=st.session_state.check_out
    
        st.text(hotel_id)
        st.text(hotel_name)
        st.text(number_of_guests)
        st.text(guests_names)
        st.text(price)
        st.text(check_in_date)
        st.text(check_out_date)

if __name__=="__main__":
    confirm_hotel_booking()
