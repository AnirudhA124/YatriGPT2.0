import streamlit as st
import base64
import os
from pathlib import Path

st.set_page_config(
    page_title="Home",
    initial_sidebar_state="collapsed"
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
        image_path = Path(f"C:/Users/Anirudh/Desktop/Python Internship/Project/YatriGPT/backend/data/images/{username}.jpg")
        
        # Alternative: put images in streamlit's static folder
        # image_path = Path(f"static/images/{username}.jpg")
        
        if image_path.exists():
            with open(image_path, "rb") as img_file:
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
        
        st.title(f"Welcome {name}")

if __name__ == "__main__":
    home_page()