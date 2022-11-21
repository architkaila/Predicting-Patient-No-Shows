## Library relevant imports
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from streamlit import runtime
import datetime
import sqlite3

import data_explorer
import patient_predictor
import about_us
import neighbourhood_analysis

@st.cache
def load_data():
    """ Loads the required dataframe into the webapp """

    ## Make a connection to the databse
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    ## Read data from the database
    df = pd.read_sql_query("SELECT * FROM final_data_for_modelling", conn)

    df["scheduledday"] = pd.to_datetime(df["scheduledday"], format='%Y-%m-%d %H:%M:%S')
    df["appointmentday"] = pd.to_datetime(df["appointmentday"], format='%Y-%m-%d %H:%M:%S')

    df_f_scores = pd.read_sql_query("SELECT * FROM f_scores_weather", conn)
    df_f_scores["F-Score"] = round(df_f_scores["F-Score"], 1)

    print("[INFO] Data is loaded")

    return df, df_f_scores


## create dataframe from the load function 
df, df_f_scores = load_data()

##########################################################################################
## Start building Streamlit App
##########################################################################################

PAGES = [
    'General Data Explorer',
    'Neighbourhood Analysis',
    'Patient Predictor',
    'About Us'
]

def run_UI():
    st.sidebar.title('Patient NoShow Analysis')
    if st.session_state["page"]:
        page=st.sidebar.radio('Navigation', PAGES, index=st.session_state["page"])
    else:
        page=st.sidebar.radio('Navigation', PAGES, index=0)

    st.experimental_set_query_params(page=page)


    if page == 'About Us':
        st.sidebar.write("""
            ## About
            
            About Us
        """)
        st.title("About Us")
        about_us.about_us_UI()

    elif page == 'Patient Predictor':
        st.sidebar.write("""
            ## About

            Accurately predicting patient ‘no-shows’ has many implications. 
            
            Identifying causes of missed appointments could inform interventions that target vulnerable demographic groups, increase accessibility to clinics, or improve patient-provider communication.
            
            An accurate prediction of whether an appointment may be missed could allow clinics and hospitals to develop scheduling strategies that minimize the cost of these no shows, such as double booking patients likely to not show up.     
        """)
        st.title("Patient Predictor")
        patient_predictor.patient_predictor_UI(df)

    elif page == 'Neighbourhood Analysis':
        st.sidebar.write("""
            ## About
            
            Patient no-shows are defined as “appointments that a patient neither attended or canceled on time to be reassigned to another patient”

            We aim to predict patient no-shows using clinical data from the Brazilian Health Department between November 2015 - June 2016.
        """)
        st.title("Neighbourhood Analysis")
        neighbourhood_analysis.neighbourhood_UI(df)

    else:
        st.sidebar.write("""
            ## About
            
            Patient no-shows are defined as “appointments that a patient neither attended or canceled on time to be reassigned to another patient”

            We aim to predict patient no-shows using clinical data from the Brazilian Health Department between November 2015 - June 2016.
        """)
        st.title("Patients Appointments Data")

        data_explorer.data_explorer_UI(df, df_f_scores)


if __name__ == '__main__':

    ## Load the streamlit app with Data Explorer as default page
    if runtime.exists():
        url_params = st.experimental_get_query_params()
        if 'loaded' not in st.session_state:
            if len(url_params.keys()) == 0:
                st.experimental_set_query_params(page='General Data Explorer')
                url_params = st.experimental_get_query_params()

            st.session_state.page = PAGES.index(url_params['page'][0])

        run_UI()
