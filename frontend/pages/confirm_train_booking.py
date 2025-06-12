import streamlit as st
import os
import sys
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)
from sidebar import render_sidebar
from backend.services.utils.helpers import book_train


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

def confirm_train_booking():
    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    else:
        username=st.session_state.username
        train_name=st.session_state.train_name
        train_number=st.session_state.train_number
        train_tier=st.session_state.train_tier
        number_of_seats=st.session_state.number_of_seats
        price=st.session_state.price
        render_sidebar()
        with st.form("Confirm Train Booking"):
            st.title(f"Confirm your Booking for {train_name} ({train_number}):")
            st.text(f"Train Name:{train_name}")
            st.text(f"Number of guests:{number_of_seats}")
            st.text(f"Tier:{train_tier}")
            st.text(f"Price:{price}")
            submit=st.form_submit_button("Confirm Booking & Pay Now")
            if submit:
                if book_train(number_of_seats,train_number,train_tier):
                    st.success("Booking is confirmed.")
                    with st.spinner("Redirecting to home page...."):
                        time.sleep(1)
                    st.switch_page('pages/home_page.py')
                else:
                    st.error("Booking not confirmed.")

if __name__=="__main__":
    confirm_train_booking()
