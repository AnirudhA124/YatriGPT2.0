import streamlit as st
import sys
import os
import time

# Get the absolute path to the project root (the parent of 'backend' and 'frontend')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.services.auth.auth_utils import verify_user,load_users
from backend.constants.background_imges import login_background_image

all_users=load_users()
st.set_page_config(layout="centered",initial_sidebar_state="collapsed")
st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def login():
    """Login page for web app.
    """
    page_bg_image_login=login_background_image()
    st.markdown(page_bg_image_login,unsafe_allow_html=True)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in=False
        st.session_state.username=""
        st.session_state.name=""
    st.markdown("<h1 style='text-align: center; color: white;'>YatriGPT</h1>", unsafe_allow_html=True)
    st.title("Login")
    with st.form("login_form"):
        username=st.text_input("Username",placeholder="Enter username")
        password=st.text_input("Password",placeholder="Enter password",type="password")
        submit=st.form_submit_button("Submit")
        if submit:
            if verify_user(username,password):
                st.session_state.logged_in=True
                st.session_state.username=username
                st.session_state.name=all_users[username]['name']
                
                with st.spinner("Redirecting to home page..."):
                    time.sleep(1)
                st.switch_page('pages/home_page.py')
            else:
                st.error("Invalid credentials")
    if st.button("Don't have an acount? SignUp."):
        st.switch_page('pages/signup.py')

if __name__=="__main__":
    login()
