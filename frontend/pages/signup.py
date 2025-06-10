import streamlit as st
import os
import sys
from streamlit_phone_number import st_phone_number
import time

# Fixed path calculation
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
from backend.services.auth.auth_utils import add_user
from backend.services.utils.validators import *

def signup():
    """SignUp page for web app.
    """
    page_bg_img="""
        <style>
        [data-testid="stAppViewContainer"]{
            background-image: url("https://img.freepik.com/premium-photo/outfit-accessories-equipment-traveler-black-background-with-copy-space-travel-concept_146508-635.jpg");
            background-size:cover;
        }
        </style>
    """
    st.markdown(page_bg_img,unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white;'>YatriGPT</h1>", unsafe_allow_html=True)
    st.title("SignUp")
    with st.form("SignUp_form"):
        name=st.text_input("Name",placeholder="Enter name")
        username=st.text_input("Username",placeholder="Enter username")
        email=st.text_input("Email",placeholder="Enter email")
        password=st.text_input("Password",placeholder="Enter password",type="password")
        confirm_password=st.text_input("Confirm Password",placeholder="Enter password",type="password")
        phone_number=st_phone_number("Phone Number",placeholder="Enter phone number",default_country="IN")
        preferences=st.multiselect("Preferences",['Adventure','Beaches','Temples','Mountains'])
        submit=st.form_submit_button("Submit")
        if submit:
            if name and username and email and password and confirm_password and phone_number['number'] and preferences:
                if is_valid_email(email):
                    if is_valid_phone(phone_number['nationalNumber']):
                        if is_valid_password(password):
                            if not is_username_exits(username):
                                if password==confirm_password:
                                    if add_user(name,username,password,email,phone_number['nationalNumber'],preferences):
                                        st.success("User added.")
                                        with st.spinner("Redirecting to login..."):
                                            time.sleep(1)
                                        st.switch_page('main.py')
                                    else:
                                        st.error("User not added.")                                        
                                else:
                                    st.error("Password and confirm password not same.")
                            else:
                                st.error("Username already used.")
                        else:
                            st.error("Enter valid password.")
                    else:
                        st.error("Enter valid number.")
                else:
                    st.error("Enter valid email.")
            else:
                st.error("Please fill all fields.")

if __name__=="__main__":
    signup()
