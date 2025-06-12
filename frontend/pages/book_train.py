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
        st.session_state.train_number=""
        st.session_state.train_tier=""
        st.session_state.train_name=""
        st.session_state.number_of_seats=None
        st.session_state.price=None

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
    number_of_seats=st.selectbox("Number of Seats",[1,2,3,4,5])

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

            class_options = [f"{cls['name']} (₹{cls['fare']}, {cls['available']} seats)" for cls in train['classes']]
            selected_class = st.radio(
                "Select Class",
                options=class_options,
                key=f"train_{train['train_number']}_class"
            )

            selected_class_name = selected_class.split(' (')[0] if selected_class else None

            if st.button("Book Now", key=f"book_{train['train_number']}"):
                st.session_state.train_name=train['train_name']
                st.session_state.train_number=train['train_number']
                st.session_state.train_tier=selected_class_name
                st.session_state.number_of_seats=number_of_seats
                for cls in train['classes']:
                    if cls['name']==selected_class_name:
                        st.session_state.price=cls['fare']*number_of_seats
                st.switch_page('pages/confirm_train_booking.py')
                


if __name__ == "__main__":
    book_train()
