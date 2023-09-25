import streamlit as st
import pandas as pd
import numpy as np

#from streamlit_elements import elements, mui, html
#import streamlit_authenticator as stauth
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    # Page title
    st.set_page_config(page_title='IAC-Rutting Verification')

    # sidebar
    with st.sidebar:
        st.title("TxDOT Inter-Agency Contract")
        st.subheader("Rutting Measurement Verification")
        st.text("Maintenance Devision")
        st.text("Presented by Hongbin Xu and Jorge Prozzi")
        st.text("The University of Texas at Austin")
    
    # Mysql connection
    conn = st.experimental_connection('mysql', type='sql')
    col1, col2 = st.columns([3,4])
    with col1:
        with st.container():
            st.subheader("Suface")
            col11, col12 = st.columns(2)
            with col11:
                segID = st.number_input("Segment ID", min_value=1, max_value=100, step= 1)
            with col12:
                scanID = st.number_input("Scan ID", min_value=0, max_value=899, step = 1)
            #data = pd.
    
            with st.container():
                # Some number in the range 0-23
                hour_to_filter = st.slider('hour', 0, 23, 17)
                filtered_data = data1[data1[DATE_COLUMN].dt.hour == hour_to_filter]
                st.map(filtered_data)
    
    with col2:
        with st.container():
            st.subheader("Transverse Profile")   
            hist_values = np.histogram(data1[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
            st.bar_chart(hist_values)
            if st.checkbox('Show raw transverse profile data'):
                st.write(data1)
    
    
    
