## Library relevant imports
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from constants import NEIGHBOURHOODS

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure

def data_explorer_UI(df, df_f_scores):

    ## Generate view metrics
    total_num_of_appointments = len(df)
    unique_patient_count = df.patientid.nunique()
    avg_wait_peroid = round(df.days_between_appointment_and_scheduled_day.mean(),0)
    female_male_ratio = round(df.query('gender == "F"').gender.count() / df.query('gender == "M"').gender.count(), 1)

    count_shows = df["showed"].value_counts()[1]
    count_no_shows = df["showed"].value_counts()[0]
    showup_percent = round( (count_shows/total_num_of_appointments)*100, 1)
    no_showup_percent = round( (count_no_shows/total_num_of_appointments)*100, 1)
    

    data_to_plot = {
        "Total Appointments":total_num_of_appointments,
        "Num of ShowUp's":count_shows,
        "Num of No ShowUp's":count_no_shows,
        "Avg Waiting Peroid":str(avg_wait_peroid) + " days",
        "Total Patients":unique_patient_count,
        "Patient ShowUp %":str(showup_percent) + " %",
        "Patient No ShowUp %":str(no_showup_percent) + " %",
        "Female / Male Ratio":female_male_ratio,
    }



    ## Add view cards for basic information around data
    col1, col2, col3, col4 = st.columns(4)
    columns = [col1, col2, col3, col4]
    
    count = 0
    for key, value in data_to_plot.items():
        with columns[count]:
            st.metric(label= key, value = value)
            count += 1
            if count >= 4:
                count = 0

    # st.write('''  

    #     ### Neighbourhood Analysis
    #     Our data from brazil contains 81 unique neighbourhood areas. Choose one for EDA.       
    #     ''')
    # state = st.selectbox("Select a neighbourhood", NEIGHBOURHOODS).strip()
    # print(state)

    st.markdown("""---""")

    matplotlib.use("agg")
    _lock = RendererAgg.lock
    sns.set_style("darkgrid")

    row_1_col1, row_1_col2 =  st.columns(2)
    with row_1_col1, _lock:
        st.subheader("Patients Appointment Show (vs) NoShow")
        ## Pie chart to explore distribution of shows and no shows
        fig = Figure()
        ax = fig.subplots()
        df["showed"].value_counts().plot(kind="pie", autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)

    with row_1_col2, _lock:
        st.subheader("Appointments by Day of Week")

        ## bar chart to explore distribution of appointments across days of week
        weekday_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        fig = Figure()
        ax = fig.subplots()
        sns.countplot(x=df.appointment_day_of_week, order=weekday_names, ax=ax)
        st.pyplot(fig)
    
    st.markdown("""---""")
    row_2_col1, row_2_col2 =  st.columns(2)
    with row_2_col1, _lock:
        st.subheader("KDE plot of age feature")
        ## KDE plot of age
        fig = Figure()
        ax = fig.subplots()
        sns.kdeplot(df["age"], bw=None, ax=ax)
        st.pyplot(fig)

    with row_2_col2, _lock:
        st.subheader("KDE plot of waiting time")

        ## kde plot of days_between_appointment_and_scheduled_day
        fig = Figure()
        ax = fig.subplots()
        sns.kdeplot(df["days_between_appointment_and_scheduled_day"], bw=None, ax=ax)
        st.pyplot(fig)

    st.markdown("""---""")
    row_3_col1, row_3_col2 =  st.columns(2)
    with row_3_col1, _lock:
        st.subheader("Waiting period (vs) ShowUp")

        ## High wait peroid has direct relation with higher no show ups

        ## Average of waiting peroid
        avg_waiting_days = round(df.days_between_appointment_and_scheduled_day.mean(), 0)

        ## Patients with less than waiting period
        less_waiting_days = df.query(f'days_between_appointment_and_scheduled_day <= {avg_waiting_days}')
        # Calculating percentage of people who showed up and waiting time less than AVG waiting time
        less_waiting_percent = round((less_waiting_days.query('showed == 1').showed.count()/less_waiting_days.showed.count())*100, 1)
        
        ## Patients with longer than waiting period
        longer_waiting_days = df.query(f'days_between_appointment_and_scheduled_day > {avg_waiting_days}')
        # Calculating percentage of people who showed up and waiting time longer than AVG waiting time
        longer_wait_percent=round((longer_waiting_days.query('showed == 1').showed.count()/longer_waiting_days.showed.count())*100, 1)
        
        # for index, value in enumerate([less_waiting_percent,longer_wait_percent]):
        #     plt.text(value, index, str(round(value,1)))
        fig = Figure()
        ax = fig.subplots()

        data_to_plott = pd.DataFrame({"Waiting Time":["LESS than average waiting time", "LONGER then average waiting time"],
                            "ShowUp %":[less_waiting_percent, longer_wait_percent]})
        sns.barplot(data=data_to_plott, x="Waiting Time", y="ShowUp %", ax=ax)
        ax.bar_label(ax.containers[0])
        st.pyplot(fig)

    with row_3_col2, _lock:
        st.subheader("Age Group (vs) ShowUp %")

        ## Age wrt to apoointments show up %

        # Different age groups to explore

        age_groups=["infants", "children", "youth", "adults", "seniors"]

        # Total number of patients belonging to each age group
        age_count_by_group = df.groupby("age_group").showed.count()
        # Numbers of pateints who showed up in each age group
        age_count_by_group_showup = df.groupby('age_group').showed.sum()
        # Calculating show up % by each age group
        data_to_plot_age_groups = pd.DataFrame(round((age_count_by_group_showup / age_count_by_group), 3)*100).reindex(age_groups).reset_index().rename(columns={"showed":"ShowUp %"})

        ## Plot chart
        fig = Figure()
        ax = fig.subplots()

        sns.barplot(data=data_to_plot_age_groups, x="age_group", y="ShowUp %", ax=ax)
        ax.bar_label(ax.containers[0])
        st.pyplot(fig)
    
    st.markdown("""---""")
    row_4_col1, row_4_col2 =  st.columns(2)
    with row_4_col1, _lock:
        st.subheader("Disability (vs) ShowUp %")

        ## Physical disablity has direct relation with higher show ups

        # % of handicap people who showed up
        handicap_percent = (df.query('handicap > 0 & showed == 1').showed.count() / df.query('handicap == 1').showed.count())*100
        # % of non handicap people who showed up
        not_handicap_percent = (df.query('handicap == 0 & showed == 1').showed.count() / df.query('handicap == 0').showed.count())*100
        
        ## Plot the figure
        fig = Figure()
        ax = fig.subplots()

        data_to_plot_handicap = pd.DataFrame({"Patients":["Handicapped", "Not Handicapped"],
                                                "ShowUp %":[handicap_percent, not_handicap_percent]})
        sns.barplot(data=data_to_plot_handicap, x="Patients", y="ShowUp %", ax=ax)
        ax.bar_label(ax.containers[0])
        st.pyplot(fig)


    with row_4_col2, _lock:
        st.subheader("Gender Distribution")

        ## Gender relation with higher show ups        
        ## Plot the figure
        fig = Figure()
        ax = fig.subplots()
        
        sns.countplot(data=df, x="gender",hue="showed", ax=ax)

        for container in ax.containers:
            ax.bar_label(container)

        #ax.bar_label(ax.containers[0])
        st.pyplot(fig)
    
    st.markdown("""---""")
    row_5_col1, row_5_col2 =  st.columns(2)
    with row_5_col1, _lock:
        st.subheader("Reminder (vs) ShowUp%")
        
        ## SMS reminder vs Show Up %
        sms_percent = round((df.query('sms_received == 1 & showed == 1').showed.count() / df.query('sms_received == 1').showed.count()), 3)*100
        no_sms_percent = round((df.query('sms_received == 0 & showed == 1').showed.count() / df.query('sms_received == 0').showed.count()), 3)*100


        data_to_plott_sms = pd.DataFrame({"Reminder":["SMS recieved", "No SMS recieved"],
                            "ShowUp %":[no_sms_percent, sms_percent]})       
        ## Plot the figure
        fig = Figure()
        ax = fig.subplots()

        sns.barplot(data=data_to_plott_sms, x="Reminder", y="ShowUp %", ax=ax)

        ax.bar_label(ax.containers[0])
        st.pyplot(fig)
    
    with row_5_col2, _lock:
        st.subheader("Scholarship (vs) ShowUp%")

        ## Scholarship vs Show Up %
        scholarship_percent = (df.query('scholarship == 1 & showed == 1').showed.count() / df.query('scholarship == 1').showed.count())*100
        no_scholarship_percent = (df.query('scholarship == 0 & showed == 1').showed.count() / df.query('scholarship == 0').showed.count())*100

        data_to_plott_sms = pd.DataFrame({"Scholarship":["Available", "Not Available"],
                            "ShowUp %":[scholarship_percent, no_scholarship_percent]})
        
        ## Plot the figure
        fig = Figure()
        ax = fig.subplots()

        sns.barplot(data=data_to_plott_sms, x="Scholarship", y="ShowUp %", ax=ax)

        ax.bar_label(ax.containers[0])
        st.pyplot(fig)

    st.markdown("""---""")

    with st.container():
        st.subheader("Weather feature analysis")

        ## Plot the figure
        fig = Figure()
        ax = fig.subplots()

        sns.barplot(data=df_f_scores, x="Feature", y="F-Score", ax=ax)

        ax.bar_label(ax.containers[0])
        ax.set_xticklabels(df_f_scores["Feature"], rotation=45) 
        st.pyplot(fig)




