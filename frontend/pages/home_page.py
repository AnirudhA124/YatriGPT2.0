import streamlit as st

def home_page():
    """Home Page for the web app.
    """
    if not st.session_state.get('logged_in'):
        st.switch_page("main.py")
    st.title(f"Welcome {st.session_state.name}")

if __name__=="__main__":
    home_page()
