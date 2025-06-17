import os
import sys
import streamlit as st
from backend.services.utils.helpers import get_trains
from backend.services.utils.validators import is_valid_phone
from sidebar import render_sidebar
import datetime

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
        st.session_state.train_number = ""
        st.session_state.train_tier = ""
        st.session_state.train_name = ""
        st.session_state.number_of_seats = None
        st.session_state.price = None
        st.session_state.travel_date = None

    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    render_sidebar()
    st.title("Train Booking")
    if 'username' not in st.session_state:
        st.error("Please log in to book a train.")
        return

    username = st.session_state.username
    places = ["Goa", "Shimla", "Jaipur", "Darjeeling", "Kerela", "Delhi", "Indore"]
    source = st.selectbox("Source", places)
    destination = st.selectbox("Destination", [place for place in places if place != source])
    number_of_seats = st.selectbox("Number of Seats", [1, 2, 3, 4, 5])
    travel_date = st.date_input("Travel Date", value="today", min_value="today")
    # Fetch train data
    train_data = get_trains()

    # Filter trains by source, destination, and date
    filtered_trains = [
        train for train in train_data['trains']
        if (
            train['from'] == source
            and train['to'] == destination
            and datetime.datetime.fromisoformat(train['departure']).date() == travel_date
        )
    ]

    # --- FILTER BY CLASS ---
    # Get all unique class names across filtered trains
    all_classes = set()
    for train in filtered_trains:
        for cls in train['classes']:
            all_classes.add(cls['name'])
    all_classes = sorted(list(all_classes))
    all_classes.insert(0, "All")  # Add "All" option

    selected_class = st.selectbox("Filter by Class", all_classes)

    # Filter trains to only those with the selected class (if not "All")
    filtered_trains_by_class = []
    for train in filtered_trains:
        if selected_class == "All":
            filtered_trains_by_class.append(train)
        else:
            for cls in train['classes']:
                if cls['name'] == selected_class:
                    filtered_trains_by_class.append(train)
                    break

    # --- SORT BY PRICE ---
    # Calculate min price for each train (for sorting)
    train_min_prices = []
    for train in filtered_trains_by_class:
        if selected_class == "All":
            min_price = min([cls['fare'] for cls in train['classes']])
        else:
            min_price = next((cls['fare'] for cls in train['classes'] if cls['name'] == selected_class), float('inf'))
        train_min_prices.append(min_price)

    # Sort trains by min price
    sort_order = st.radio("Sort by Price", ["Lowest to Highest", "Highest to Lowest"], horizontal=True)
    if sort_order == "Lowest to Highest":
        sorted_trains = [train for _, train in sorted(zip(train_min_prices, filtered_trains_by_class))]
    else:
        sorted_trains = [train for _, train in sorted(zip(train_min_prices, filtered_trains_by_class), reverse=True)]

    # --- DISPLAY TRAINS ---
    for train in sorted_trains:
        with st.container(border=True):
            st.subheader(train['train_name'])
            st.write(f"Train Number: {train['train_number']}")
            st.write(f"From: {train['from']} | To: {train['to']}")
            st.write(f"Departure: {train['departure']}")
            st.write(f"Arrival: {train['arrival']}")
            st.write(f"Travel Time: {train['travel_time']}")
            st.write("**Available Classes:**")

            # Show only relevant classes if filtered
            shown_classes = (
                [cls for cls in train['classes'] if cls['name'] == selected_class]
                if selected_class != "All"
                else train['classes']
            )

            class_options = [
                f"{cls['name']} (₹{cls['fare']}, {cls['available']} seats)"
                for cls in shown_classes
            ]
            selected_class_radio = st.radio(
                "Select Class",
                options=class_options,
                key=f"train_{train['train_number']}_class"
            )

            if selected_class_radio:
                selected_class_name = selected_class_radio.split(' (')[0]

                if st.button("Book Now", key=f"book_{train['train_number']}"):
                    st.session_state.selected_train_id=train['train_number']
                if st.session_state.selected_train_id==train['train_number']:
                    with st.form(f'book_{train['train_number']}',enter_to_submit=False):
                        name=st.text_input("Name",placeholder="Enter full name")
                        guest_names=[name]
                        for i in range(number_of_seats-1):
                            guest_name=st.text_input(f"Passenger {i+1} Name",placeholder="Enter full name")
                            guest_names.append(guest_name)
                        phone_number=st.text_input("Phone Number",placeholder="Enter phome number")
                        submit=st.form_submit_button("Submit")
                        if submit:
                            if name and guest_names and phone_number:
                                if is_valid_phone(phone_number):
                                    st.session_state.guest_names=guest_names
                                    st.session_state.phone_number=phone_number
                                    st.session_state.train_name = train['train_name']
                                    st.session_state.train_number = train['train_number']
                                    st.session_state.train_tier = selected_class_name
                                    st.session_state.number_of_seats = number_of_seats
                                    st.session_state.travel_date = travel_date
                                    for cls in train['classes']:
                                        if cls['name'] == selected_class_name:
                                            st.session_state.price = cls['fare'] * number_of_seats
                                            break
                                    st.switch_page('pages/confirm_train_booking.py')
                                else:
                                    st.error("Enter valid phone number.")
                            else:
                                st.error("Enter all fields.")
                    

if __name__ == "__main__":
    book_train()
