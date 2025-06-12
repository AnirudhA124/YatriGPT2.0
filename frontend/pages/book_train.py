import os
import sys
import streamlit as st
from backend.services.utils.helpers import get_trains
from backend.services.utils.validators import is_valid_phone
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
def book_train():
    if "selected_train_id" not in st.session_state:
        st.session_state.selected_train_id = None

    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    render_sidebar()
    st.title("Train Booking")
    if 'username' not in st.session_state:
        st.error("Please log in to book a hotel.")  # Note: Should say "train" if booking trains
        return

    username = st.session_state.username
    places = ["Goa", "Shimla", "Jaipur", "Darjeeling", "Kerela", "Delhi", "Indore"]
    source = st.selectbox("Source", places)
    destination = st.selectbox("Destination", [place for place in places if place != source])

    # Fetch train data
    train_data = get_trains()

    # Filter trains by source and destination
    filtered_trains = [train for train in train_data['trains'] 
                       if train['from'] == source and train['to'] == destination]

    # Display each train in a container with availability and prices
    for train in filtered_trains:
        with st.container(border=True):
            st.subheader(train['train_name'])
            st.write(f"Train Number: {train['train_number']}")
            st.write(f"From: {train['from']} | To: {train['to']}")
            st.write(f"Departure: {train['departure']}")
            st.write(f"Arrival: {train['arrival']}")
            st.write(f"Travel Time: {train['travel_time']}")
            st.write("**Available Classes:**")
            for cls in train['classes']:
                st.write(f"- {cls['name']}: {cls['available']} seats available")
                st.write(f"Price: ₹{cls['fare']}")

if __name__ == "__main__":
    book_train()
