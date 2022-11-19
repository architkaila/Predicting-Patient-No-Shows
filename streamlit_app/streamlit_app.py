## Library relevant imports
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from streamlit import runtime
import datetime

import data_explorer
import patient_predictor
import about_us
import neighbourhood_analysis

@st.cache
def load_data():
    """ Loads the required dataframe into the webapp """

    df = pd.read_csv('./streamlit_app/data/final_data_for_modelling.csv')

    df["scheduledday"] = pd.to_datetime(df["scheduledday"], format='%Y-%m-%d %H:%M:%S')
    df["appointmentday"] = pd.to_datetime(df["appointmentday"], format='%Y-%m-%d %H:%M:%S')


    print("[INFO] Data is loaded")

    return df


# create dataframe from the load function 
df = load_data()


###############################################################################
## Start building Streamlit App
###############################################################################

PAGES = [
    'General Data Explorer',
    'Neighbourhood Analysis',
    'Patient Predictor',
    'About Us'
]

def run_UI():
    st.sidebar.title('Patient No Show Predictor')
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

            Accurately predicting patient ‘no-shows’ has many implications. Identifying causes of missed appointments could inform interventions that target vulnerable demographic groups, increase accessibility to clinics, or improve patient-provider communication. Moreover, an accurate prediction of whether an appointment may be missed could allow clinics and hospitals to develop scheduling strategies that minimize the cost of these no shows, such as double booking patients likely to not show up.     
        """)
        st.title("Patient Predictor")
        patient_predictor.patient_predictor_UI(df)

    elif page == 'Neighbourhood Analysis':
        st.sidebar.write("""
            ## About

            Accurately predicting patient ‘no-shows’ has many implications. Identifying causes of missed appointments could inform interventions that target vulnerable demographic groups, increase accessibility to clinics, or improve patient-provider communication. Moreover, an accurate prediction of whether an appointment may be missed could allow clinics and hospitals to develop scheduling strategies that minimize the cost of these no shows, such as double booking patients likely to not show up.     
        """)
        st.title("Neighbourhood Analysis")
        neighbourhood_analysis.neighbourhood_UI(df)

    else:
        st.sidebar.write("""
            ## About
            
            Globally, the delivery of healthcare is constrained by a supply shortage of trained providers and infrastructure. The demands placed on healthcare systems continue to rise as populations grow and age1. The pandemic has exposed and further exacerbated this strain on our hospitals, clinics and healthcare providers; it is now more important than ever to develop systems that efficiently allocate resources, minimize cost and keep our patients healthy.
        """)
        st.title("Patients Appointments Data")

        data_explorer.data_explorer_UI(df)


if __name__ == '__main__':

    if runtime.exists():
        url_params = st.experimental_get_query_params()
        if 'loaded' not in st.session_state:
            if len(url_params.keys()) == 0:
                st.experimental_set_query_params(page='General Data Explorer')
                url_params = st.experimental_get_query_params()

            st.session_state.page = PAGES.index(url_params['page'][0])

        run_UI()
    # subcol_1, subcol_2 = st.columns(2)
    # with subcol_1:
    #     st.session_state.data_type = st.radio("Data resolution:", ('County Level', 'Census Tracts'), index=0)
    # with subcol_2:
    #     # Todo: implement for census level too
    #     if st.session_state.data_type =='County Level':
    #         st.session_state.data_format = st.radio('Data format', ['Raw Values', 'Per Capita', 'Per Square Mile'], 0)

    # if st.session_state.data_type == 'County Level':
    #     data_explorer.county_data_explorer()
    # else:
    #     data_explorer.census_data_explorer()
