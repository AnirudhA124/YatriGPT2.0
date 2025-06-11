import streamlit as st
import base64
import os
import time
from pathlib import Path
from streamlit_card import card
from backend.constants.background_imges import (cover_image,book_hotel,book_flight,book_train,
                                                restaurants,itinerary,activities)

st.set_page_config(
    page_title="Home",
    initial_sidebar_state="collapsed",
    layout='wide'
)

# CSS for profile image
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

def load_profile_image(username):
    """Load and encode profile image as base64"""
    try:
        # Use relative path or put images in a 'static' folder
        image_path_jpg = Path(f"C:/Users/Anirudh/Desktop/Python Internship/Project/YatriGPT/backend/data/images/{username}.jpg")
        image_path_png = Path(f"C:/Users/Anirudh/Desktop/Python Internship/Project/YatriGPT/backend/data/images/{username}.png")
        image_path_jpeg = Path(f"C:/Users/Anirudh/Desktop/Python Internship/Project/YatriGPT/backend/data/images/{username}.jpeg")
        
        # Alternative: put images in streamlit's static folder
        # image_path = Path(f"static/images/{username}.jpg")
        
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

def home_page():
    """Home Page for the web app."""
    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    else:
        name = st.session_state.get('name', 'User')
        username = st.session_state.get('username', 'user')
        
        with st.sidebar:
            st.markdown('<h2 class="centered-header">👤 User Profile</h2>', unsafe_allow_html=True)
            
            # Try to load profile image
            profile_img_data = load_profile_image(username)
            
            if profile_img_data:
                st.markdown(
                    f'<img src="data:image/jpeg;base64,{profile_img_data}" class="profile-img">', 
                    unsafe_allow_html=True
                )
            else:
                # Show placeholder with user's initial
                initial = name[0].upper() if name else 'U'
                st.markdown(
                    f'<div class="profile-placeholder">{initial}</div>', 
                    unsafe_allow_html=True
                )
            
            st.markdown(
                f'<div class="centered-username">@{username}</div>', 
                unsafe_allow_html=True
            )

            logout=st.button("Logout",use_container_width=True)
            if logout:
                st.session_state.logged_in=False
                st.session_state.username=""
                st.session_state.name=""
                st.switch_page('main.py')
        
        custom_html = cover_image()
        # Display the custom HTML
        st.markdown(
                custom_html, 
                unsafe_allow_html=True
            )
        st.title(f"Welcome {name}")

        # Show spinner while loading cards
        with st.spinner('Loading booking options...'):            
            col1,col2,col3=st.columns(3)

            with col1:
                if card(title="Book Hotels",text="Book Hotels",key="hotels",image=book_hotel()):
                    st.switch_page('pages/book_hotel.py')
                if card(title="Book Train",text="Book Trains",key="train",image=book_train()):
                    pass
            with col2:
                if card(title="Itinerary",text="Generate your itinerary",key="itinerary",image=itinerary()):
                    pass
                if card("Book Flights",text="Book flights",key="flight",image=book_flight()):
                    pass
            with col3:
                if card(title="Nearby Restaurants",text="Reserve your seat",key="restaurant",image=restaurants()):
                    pass
                if card(title="Activities",text="Book exciting activities",key="activities",image=activities()):
                    pass

if __name__ == "__main__":
    home_page()