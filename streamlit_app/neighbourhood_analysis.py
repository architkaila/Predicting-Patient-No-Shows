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

def neighbourhood_UI(df):

    st.write('''  
        ### Overall Analysis Across Neighbourhoods      
        ''')
    
    ## Generate view metrics
    total_num_of_appointments = len(df)
    num_of_neighbourhoods = df.neighbourhood.nunique()
    avg_wait_peroid = round(df.days_between_appointment_and_scheduled_day.mean(),0)

    count_shows = df["showed"].value_counts()[1]
    count_no_shows = df["showed"].value_counts()[0]
    showup_percent = round( (count_shows/total_num_of_appointments)*100, 1)
    no_showup_percent = round( (count_no_shows/total_num_of_appointments)*100, 1)
    

    data_to_plot = {
        "Neighbourhoods":str(num_of_neighbourhoods),
        "Avg Waiting Peroid":str(avg_wait_peroid) + " days",
        "Patient ShowUp %":str(showup_percent) + " %",
        "Patient No ShowUp %":str(no_showup_percent) + " %",
    }

    ## Add view cards for basic information around data
    col1, col2, col3, col4 = st.columns(4)
    columns = [col1, col2, col3, col4]
    
    count = 0
    for key, value in data_to_plot.items():
        with columns[count]:
            st.metric(label= key, value = value)
            count += 1

    matplotlib.use("agg")
    _lock = RendererAgg.lock
    sns.set_style("darkgrid")

    st.markdown("""---""")

    with st.container():
        neighbourhood_selected = st.selectbox("Select a neighbourhood", NEIGHBOURHOODS).strip()
    
    ## Generate view metirc row 2
    # Patients from selected nieghbourhood
    df_filtered_neigh = df[df['neighbourhood'] == neighbourhood_selected].copy()
    patients_from_neigh = len(df_filtered_neigh)

    # Avg wait time for selcted neighbourhood
    waitint_time_by_neighbourhood = df.groupby('neighbourhood').days_between_appointment_and_scheduled_day.mean()
    avg_wait_selected_neigh = round(waitint_time_by_neighbourhood[neighbourhood_selected], 1)

    # Rating of neighbourhood
    rating = round(np.mean(df_filtered_neigh["rating"]),1)

    count_shows = df_filtered_neigh["showed"].value_counts()[1]
    count_no_shows = df_filtered_neigh["showed"].value_counts()[0]
    showup_percent = round( (count_shows/patients_from_neigh)*100, 1)
    no_showup_percent = round( (count_no_shows/patients_from_neigh)*100, 1)
    
    data_to_plot_row2 = {
        "Avg Waiting time":str(avg_wait_selected_neigh) + " days",
        "Total Patients":str(patients_from_neigh),
        "Patient No ShowUp %":str(no_showup_percent) + " %",
        "Rating":str(rating),
    }

    ## Add view cards for basic information around data
    col1, col2, col3, col4 = st.columns(4)
    columns = [col1, col2, col3, col4]
    
    count = 0
    for key, value in data_to_plot_row2.items():
        with columns[count]:
            st.metric(label= key, value = value)
            count += 1

    ## Weather Analysis by Neighbourhood
    ## Exploring effect of different weather parameters on patient show ups in each neighbourhood
    weather_cols = ['humidity', 'feelslikemax', 'windspeed', 'solarradiation']
    appointments_weather_df = df.groupby(['neighbourhood','showed'])[weather_cols].mean().reset_index()

    patient_no_show_weather = appointments_weather_df[appointments_weather_df["neighbourhood"] == neighbourhood_selected]
    patient_no_show_weather.showed = patient_no_show_weather.showed.astype("str")

    col1, col2 = st.columns(2)
    columns = [col1, col2]
    
    count = 0
    for i, col_name in enumerate(weather_cols):
        with columns[count]:
            
            ## Plot bar chart
            fig = Figure()
            ax = fig.subplots()

            data_to_plot_weather = patient_no_show_weather.copy()[["showed", col_name]]

            sns.barplot(data=data_to_plot_weather, x="showed", y=col_name, ax=ax, width=0.5)

            ax.bar_label(ax.containers[0])
            st.pyplot(fig)

            count += 1
            if count >= 2:
                count = 0

            # axs[i, j].bar(patient_no_show_weather["showed"], patient_no_show_weather[columns[col_idx]], width = 0.25)
            # axs[i, j].set_ylabel(columns[col_idx])
            # axs[i, j].set_xticks([0, 1], ['No Show', 'Show'])
    
        
    # with row_1_col1:
    #     st.subheader("Average Waiting Time For Each Neighbourhood")

    #     ## Avg waiting time for each neighbourhood
    #     waitint_time_by_neighbourhood = df.groupby('neighbourhood').days_between_appointment_and_scheduled_day.mean()

    #     fig = Figure(figsize=(6, 18))
    #     ax = fig.subplots()

    #     data_to_plott_neighbourhood_avg = pd.DataFrame(waitint_time_by_neighbourhood).reset_index().rename(columns={"neighbourhood":"Neighbourhoods", "days_between_appointment_and_scheduled_day":"Avg Weight Time"})
    #     data_to_plott_neighbourhood_avg["Avg Weight Time"] = round(data_to_plott_neighbourhood_avg["Avg Weight Time"], 1)

    #     sns.barplot(data=data_to_plott_neighbourhood_avg, x="Avg Weight Time", y="Neighbourhoods", ax=ax)
        
    #     ax.bar_label(ax.containers[0])
    #     st.pyplot(fig)
