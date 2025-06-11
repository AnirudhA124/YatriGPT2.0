import os
import sys
import streamlit as st

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.services.utils.helpers import get_hotels

def book_hotel():
    st.title("Hotel Booking")
    username=st.session_state.username
    hotel_data=get_hotels()
    places_name=[place['name'] for place in hotel_data['places']]
    selected_place=st.selectbox("Select a place",places_name)
    selected_place_data = None
    for place in hotel_data['places']:
        if place['name'] == selected_place:
            selected_place_data = place
            break
    if selected_place_data:
        st.subheader(f'Hotels in {selected_place}:')
        for hotel in selected_place_data['hotels']:
            with st.container(border=True):
                st.subheader(f'{hotel['name']}')
                st.write(f'Price: ₹{hotel['price']}')
                full_stars = int(hotel['rating'])
                stars = "⭐" * full_stars + (5-full_stars)*'☆'
                st.write(f"Rating: {stars} ({hotel['rating']})")
                st.write(f"Amenities: {', '.join(hotel['amenities'])}")
                if st.button("Book", key=f"book_{hotel['id']}"):
                    pass

    else:
        st.error("No hotels found for the selected place.")           

if __name__=="__main__":
    book_hotel()
