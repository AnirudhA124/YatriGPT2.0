import streamlit as st
import os
import sys
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)
from sidebar import render_sidebar
from backend.services.utils.helpers import get_trip_history


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

def trip_history():
    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    else:
        render_sidebar()
        username=st.session_state.username
        trip_history=get_trip_history()
        for user in trip_history:
            if user==username:
                trip_plans=trip_history[user]
                for trip in trip_plans:
                    with st.container(border=True):
                        st.header(f"Trip to {trip['place']}")
                        st.markdown(f"**Trip to:** {trip['place']}")
                        for i, day in enumerate(trip['itinerary'], 1):
                            st.write(f"**Day {i}:** {day}")
        if username not in trip_history:
            st.title("No Trips Planned!")
        

if __name__=="__main__":
    trip_history()