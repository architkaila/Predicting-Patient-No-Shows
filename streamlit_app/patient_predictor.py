## Library relevant imports
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import datetime

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
from PIL import Image

from model import predict_patient_showup

def patient_predictor_UI(df):

    matplotlib.use("agg")
    _lock = RendererAgg.lock
    sns.set_style("darkgrid")

    ## ## provide a list of appointments available
    with st.container():
        appointmennts = df["appointmentid"].unique().astype(str)
        selected_appointment = st.selectbox("Select an Appointment ", appointmennts).strip()
    
    st.markdown("""---""")
    print()

    data_to_plot = {
        "Neighbourhood":str(df[df["appointmentid"] == int(selected_appointment)]["neighbourhood"].values[0]),
        "Scheduled Day":pd.to_datetime(str(df[df["appointmentid"] == int(selected_appointment)]["scheduledday"].values[0])).strftime("%d %b, %Y"),
        "Appointment Day":pd.to_datetime(str(df[df["appointmentid"] == int(selected_appointment)]["appointmentday"].values[0])).strftime("%d %b, %Y"),
    }

    ## Add view cards for basic information aroud appointment
    st.subheader("General Appointment Details")

    col1, col2, col3 = st.columns((3,2,2))
    columns = [col1, col2, col3]
    
    count = 0
    for key, value in data_to_plot.items():
        with columns[count]:
            st.metric(label= key, value = value)
            count += 1
    
    ## Add details about patients
    st.markdown("""---""")
    st.subheader("Patient Details")

    row_1_col1, row_1_col2 = st.columns(2)
    with row_1_col1:

        current_gender = df[df["appointmentid"] == int(selected_appointment)]["gender"].values[0]

        ## Show patient ID
        if current_gender == 'F':
            image = Image.open('streamlit_app/data/female.png')
        else:
            image = Image.open('streamlit_app/data/male.jpg')
        patient_id = str(df[df["appointmentid"] == int(selected_appointment)]["patientid"].values[0]).split(".")[0]
        st.image(image, caption = f'Patient ID: {patient_id}')
        #title = st.text_input()
        #st.metric(label= "Patient ID", value = patient_id)

    with row_1_col2:
        ## Display age
        current_age = int(df[df["appointmentid"] == int(selected_appointment)]["age"].values[0])
        age = st.slider("Patient's Age", 0, 130, current_age)

        ## display gender
        current_gender = df[df["appointmentid"] == int(selected_appointment)]["gender"].values[0]
        gender = st.radio("Patient's Gender", ('Male', 'Female'), index= 0 if current_gender=='M' else 1)

        ## display handicap status
        current_handicap = int(df[df["appointmentid"] == int(selected_appointment)]["handicap"].values[0])
        handicap = st.selectbox("Patient's Handicap status", ('Not handicapped', 'Level 1', 'Level 2', 'Level 3', 'Level 4'), index=current_handicap)
        
    ## Add details about patients medical history
    with st.container():
        st.markdown("""---""")
        st.subheader("Medical History & Other Paramaters")

        row_2_col1, row_2_col2, row_2_col3, row_2_col4 = st.columns(4)
        with row_2_col1:
            ## display hypertension
            current_hypertension = int(df[df["appointmentid"] == int(selected_appointment)]["hypertension"].values[0])
            hypertension = st.radio("Hypertension", ('No', 'yes'), index=current_hypertension)

        with row_2_col2:
            ## display diabetes
            current_diabetes = int(df[df["appointmentid"] == int(selected_appointment)]["diabetes"].values[0])
            diabetes = st.radio("Diabetes", ('No', 'yes'), index=current_diabetes)
        with row_2_col3:
            ## display alcoholism
            current_alcoholism = int(df[df["appointmentid"] == int(selected_appointment)]["alcoholism"].values[0])
            alcoholism = st.radio("Alcoholism", ('No', 'yes'), index=current_alcoholism)

        with row_2_col4:
            ## display sms reminder
            current_sms_reminder = int(df[df["appointmentid"] == int(selected_appointment)]["sms_received"].values[0])
            sms_reminder = st.radio("SMS Reminder", ('No', 'yes'), index=current_sms_reminder)

    ## Add details about patients
    with st.container():
        st.markdown("""---""")
        st.subheader("Weather History")

        row_4_col1, row_4_col2 = st.columns(2)
        with row_4_col1:
            ## Display temp max
            current_tempmax= float(df[df["appointmentid"] == int(selected_appointment)]["tempmax"].values[0])
            tempmax = st.slider("Max Temperature", df[["tempmax"]].min().values[0] - 5, df[["tempmax"]].max().values[0] + 5, current_tempmax)

            ## Display feels like max
            current_feelslikemax= float(df[df["appointmentid"] == int(selected_appointment)]["feelslikemax"].values[0])
            feelslikemax = st.slider("Max Feels Like", df[["feelslikemax"]].min().values[0] - 5, df[["feelslikemax"]].max().values[0] + 5, current_feelslikemax)

            ## Display windspeed
            current_windspeed= float(df[df["appointmentid"] == int(selected_appointment)]["windspeed"].values[0])
            windspeed = st.slider("Windspeed", df[["windspeed"]].min().values[0] - 2, df[["windspeed"]].max().values[0] + 5, current_windspeed)

        with row_4_col2:
            ## Display temp max
            current_humidity= float(df[df["appointmentid"] == int(selected_appointment)]["humidity"].values[0])
            humidity = st.slider("Humidity", df[["humidity"]].min().values[0] - 5, df[["humidity"]].max().values[0] + 5, current_humidity)

            ## Display feels like max
            current_solarradiation = float(df[df["appointmentid"] == int(selected_appointment)]["solarradiation"].values[0])
            solarradiation = st.slider("Solar Radiation Level", df[["solarradiation"]].min().values[0] - 5, df[["solarradiation"]].max().values[0] + 5, current_solarradiation)

            ## Display windspeed
            current_uvindex = float(df[df["appointmentid"] == int(selected_appointment)]["uvindex"].values[0])
            uvindex = st.slider("Current UV Index", df[["uvindex"]].min().values[0] - 1, df[["uvindex"]].max().values[0], current_uvindex)

    ## Prediction part
    with st.container():
        st.markdown("""---""")
        st.subheader("Prediction")


        if st.button('Predict'):
            ## Show output of model
            prediction = predict_patient_showup(selected_appointment, df)
            if prediction == 0:
                st.success('This Patient will ShowUp', icon="✅")
            else:
                st.warning('Patient will Not ShowUp', icon="⚠️")
        
        st.markdown("""---""")

