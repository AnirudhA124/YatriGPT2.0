import streamlit as st
import os
import sys
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)
from sidebar import render_sidebar
from backend.services.utils.helpers import get_itineraries,save_trip_plan


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

# Load the JSON data
itineraries = get_itineraries()

def itineraries_page():
    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    else:
        username = st.session_state.username
        render_sidebar()
        st.title("Plan your Trip")
        
        destination = st.selectbox("Select your destination:", ["Goa", "Shimla", "Jaipur", "Darjeeling", "Kerela", "Delhi", "Indore"])
        days = st.selectbox("Select number of days:", ["1","2","3","4", "5"])

        # Initialize session state for itinerary
        if 'itinerary' not in st.session_state:
            st.session_state.itinerary = None

        if st.button("Generate Itinerary"):
            try:
                st.session_state.itinerary = itineraries[destination][days]
                st.success("Itinerary generated!")
            except KeyError:
                st.error("No itinerary found for selected options")

        if st.session_state.itinerary:
            st.write(f"### Suggested Itinerary for {destination} ({days} days)")
            for i, day in enumerate(st.session_state.itinerary, 1):
                st.write(f"**Day {i}:** {day}")

            if st.button("Save Plan"):
                if save_trip_plan(username, destination, st.session_state.itinerary):
                    st.success("Trip saved.")
                    time.sleep(1)
                    st.switch_page('pages/home_page.py')
                else:
                    st.error("Failed to save trip")
                    
if __name__=="__main__":
    itineraries_page()