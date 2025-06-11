# sidebar.py

import streamlit as st
import base64
from pathlib import Path


def load_profile_image(username):
    """Load and encode profile image as base64"""
    try:
        image_path_jpg = Path(f"C:/Users/Anirudh/Desktop/Python Internship/Project/YatriGPT/backend/data/images/{username}.jpg")
        image_path_png = Path(f"C:/Users/Anirudh/Desktop/Python Internship/Project/YatriGPT/backend/data/images/{username}.png")
        image_path_jpeg = Path(f"C:/Users/Anirudh/Desktop/Python Internship/Project/YatriGPT/backend/data/images/{username}.jpeg")
        
        if image_path_jpg.exists():
            with open(image_path_jpg, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                return img_data
        elif image_path_png.exists():
            with open(image_path_png, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                return img_data
        elif image_path_jpeg.exists():
            with open(image_path_jpeg, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                return img_data
        else:
            return None
    except Exception as e:
        st.error(f"Error loading profile image: {str(e)}")
        return None

def render_sidebar():
    """Render the sidebar/navbar for all pages."""
    with st.sidebar:
        st.markdown('<h2 class="centered-header">👤 User Profile</h2>', unsafe_allow_html=True)
        
        username = st.session_state.get('username', 'user')
        name = st.session_state.get('name', 'User')
        profile_img_data = load_profile_image(username)
        
        if profile_img_data:
            st.markdown(
                f'<img src="data:image/jpeg;base64,{profile_img_data}" class="profile-img">', 
                unsafe_allow_html=True
            )
        else:
            initial = name[0].upper() if name else 'U'
            st.markdown(
                f'<div class="profile-placeholder">{initial}</div>', 
                unsafe_allow_html=True
            )
        
        st.markdown(
            f'<div class="centered-username">@{username}</div>', 
            unsafe_allow_html=True
        )
        
        if st.button("Previous Bookings", use_container_width=True):
            st.switch_page('pages/previous_booking.py')
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.name = ""
            st.switch_page('main.py')
