import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Authentication function
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

def dataProc(data):
    """
    creating 2d array of the depth measurement
    """
    dataArray = np.array([np.array(data["depth"][i].split(b',')).astype("float") for i in range(data.shape[0])])
    return dataArray

# Check authentication
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
    
    # MySQL connection
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
            
            # Load data
            data = conn.query('SELECT * from pathway_rawFM365_SEP13 WHERE segID =' + str(segID) +';')
            dataArray = dataProc(data) # 2D data array
            
            # plot surface
            #with st.container():
                # surface plot
                #filtered_data = data1[data1[DATE_COLUMN].dt.hour == hour_to_filter]
                #st.map(filtered_data)
    
    with col2:
        with st.container():
            st.subheader("Transverse Profile")

            # Extract transverse profile
            scanData = data.loc[data["scanID"]==scanID, ["tranStep", "depth"]].reset_index(drop=True)
            scanData_v1 = pd.DataFrame({"DIST":scanData["tranStep"][0]*np.arange(1536), "DEPTH":np.array(scanData["depth"][0].split(b",")).astype("float")})

            # Plot transverse profile
            fig = px.line(scanData_v1, x="DIST", y="DEPTH", labels = {"DIST": "DISTANCE (mm)", "DEPTH": "DEPTH (mm}"})
            st.plotly_chart(fig)
            if st.checkbox('Show raw transverse profile data'):
                st.write(scanData_v1)
    
    
    
