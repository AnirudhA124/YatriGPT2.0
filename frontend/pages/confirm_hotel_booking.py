import streamlit as st
import os
import sys
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)
from sidebar import render_sidebar
from backend.services.utils.helpers import save_hotels


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
        username=st.session_state.username
        hotel_id=st.session_state.hotel_id    
        hotel_name=st.session_state.hotel_name
        number_of_guests=st.session_state.num_guests
        guests_names=st.session_state.guest_names
        price=st.session_state.price
        check_in_date=st.session_state.check_in
        check_out_date=st.session_state.check_out
        place=st.session_state.place
        phone_number=st.session_state.phone_number
        render_sidebar()
        with st.form("Confirm Hotel Booking"):
            st.title(f"Confirm your Booking for {hotel_name}:")
            st.text(f"Hotel Name:{hotel_name}")
            st.text(f"Number of guests:{number_of_guests}")
            st.text(f"Name of guest:")
            for i in guests_names:
                st.text(i)
            st.text(f"Price:{price}")
            st.text(f"Check In Date:{check_in_date}")
            st.text(f"Check Out Date:{check_out_date}")
            submit=st.form_submit_button("Confirm Booking & Pay Now")
            if submit:
                if save_hotels(username,hotel_id,hotel_name,place,number_of_guests,guests_names,phone_number,price,str(check_in_date),str(check_out_date)):
                    st.success("Booking is confirmed.")
                    with st.spinner("Redirecting to home page...."):
                        time.sleep(1)
                    st.switch_page('pages/home_page.py')
                else:
                    st.error("Booking not confirmed.")

if __name__=="__main__":
    confirm_hotel_booking()
