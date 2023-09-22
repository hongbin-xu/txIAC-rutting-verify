import streamlit as st
import pandas as pd
import numpy as np

#from streamlit_elements import elements, mui, html
#import streamlit_authenticator as stauth

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
st.set_page_config(
    page_title='IAC-Rutting Verification', 
    )

with st.sidebar:
    st.title("TxDOT Inter-Agency Contract")
    st.subheader("Rutting Measurement Verification")
    st.text("Maintenance Devision")
    st.text("Presented by Hongbin Xu and Jorge Prozzi")
    st.text("The University of Texas at Austin")

#conn = st.experimental_connection('mysql', type='sql')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_loading = st.text('Loading data...')
data1 = load_data(10000)
data_loading.text("Done!")

col1, col2 = st.columns([3,4])

with col1:
    with st.container():
        st.subheader("Suface")
        col11, col12 = st.columns(2)
        with col11:
            segID = st.number_input("Segment ID", min_value=1, max_value=100, step= 1)
        with col12:
            scanID = st.number_input("Scan ID", min_value=0, max_value=899, step = 1)
        st.write(segID)
        #data = pd.read_csv()

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



