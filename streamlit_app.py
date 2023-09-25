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

@st.cache_data
def dataLoad(_conn, segID):
    """
    creating 2d array of the depth measurement
    """
    data = conn.query('SELECT * from pathway_rawFM365_SEP13 WHERE segID =' + str(segID) +';')
    tranStep = data["tranStep"].mean()
    lonStep = data["lonStep"].mean()
    dataArray = np.array([np.array(data["depth"][i].split(b',')).astype("float") for i in range(data.shape[0])])
    return data, tranStep, lonStep, dataArray

@st.cache_data
def scanDataExtra(segData, scanID):
    # Extract transverse profile
    scanData = segData.loc[segData["scanID"]==scanID, ["tranStep", "depth"]].reset_index(drop=True)
    scanData_v1 = pd.DataFrame({"DIST":scanData["tranStep"][0]*np.arange(1536), "DEPTH":np.array(scanData["depth"][0].split(b",")).astype("float")})
    return scanData_v1

@st.cache_data
def surfPlot(dataArray, tranStep, lonStep):
    fig = px.imshow(dataArray, origin = "lower", labels = {"x": "Transverse (mm)", "y": "Longitudinal (mm)", "color": "DEPTH (mm)"},
                    x =np.arange(1536)*tranStep,
                    y = np.arange(900)*lonStep,
                   template = "plotly_dark")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

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
    col1, col2 = st.columns(2, gap = "medium")
    with col1:
        with st.container():
            st.subheader("Suface")
            col11, col12 = st.columns(2)
            with col11:
                segID = st.number_input("Segment ID", min_value=1, max_value=100, step= 1)
            with col12:
                scanID = st.number_input("Scan ID", min_value=0, max_value=899, step = 1)
            
            # Load data
            data, tranStep, lonStep, dataArray = dataLoad(_conn=conn, segID=segID)
            
            # plot surface
            with st.container():
                surfPlot(dataArray=dataArray, tranStep=tranStep, lonStep=lonStep)
                #fig = px.imshow(dataArray, origin = "lower", labels = {"x": "Transverse (mm)", "y": "Longitudinal (mm)", "color": "DEPTH (mm)"},
                #                x =np.arange(1536)*tranStep,
                #                y = np.arange(900)*lonStep)
                #fig.update_layout(legend = {"xanchor": "right", "x": 1.08})
                #st.plotly_chart(fig)
    
    with col2:
        with st.container():
            st.subheader("Transverse Profile")

            # Extract transverse profile
            #scanData = data.loc[data["scanID"]==scanID, ["tranStep", "depth"]].reset_index(drop=True)
            #scanData_v1 = pd.DataFrame({"DIST":scanData["tranStep"][0]*np.arange(1536), "DEPTH":np.array(scanData["depth"][0].split(b",")).astype("float")})
            scanData_v1 = scanDataExtra(segData = data, scanID=scanID)
            
            # Plot transverse profile
            fig = px.line(scanData_v1, x="DIST", y="DEPTH", labels = {"DIST": "DISTANCE (mm)", "DEPTH": "DEPTH (mm}"}, template = "plotly_dark")
            st.plotly_chart(fig)

            # View and download data
            st.download_button(label="Download profile", data=scanData_v1.to_csv().encode('utf-8'), file_name="transProfile.csv", mime = "csv")
            if st.checkbox('Show raw transverse profile data'):
                st.write(scanData_v1)
        
    
    
    
