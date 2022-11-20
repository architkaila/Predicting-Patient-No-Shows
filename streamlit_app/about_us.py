## Library relevant imports
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from PIL import Image

def about_us_UI():
    st.write("""
        Globally, the delivery of healthcare is constrained by a supply shortage of trained providers and infrastructure. The demands placed on healthcare systems continue to rise as populations grow and age. It is now more important than ever to develop systems that efficiently allocate resources, minimize cost and keep our patients healthy.  

        Patient no-shows are defined as “appointments that a patient neither attended or canceled on time to be reassigned to another patient”. While 'no-shows' directly impact patient health by delaying care and interrupting treatment, they also incur a financial cost. Studies have shown that in the clinic setting, the average cost of a no-show is 196 dollars. Moreover, for a single clinic the total financial cost can surpass 2M dollars annually.
        
        Our project aims to predict patient no-shows using clinical data from the Brazilian Health Department between November 2015 - June 2016. An accurate prediction of whether an appointment may be missed could allow clinics and hospitals to develop scheduling strategies that minimize the cost of these no shows. 
        
        We are doing this project as a part of our core curriculam at Duke University for Masters in Artificial Intelligence (Course: AIPI 510: Sourcing Data for Analytics)
        """)

    st.markdown("""---""")

    st.subheader("The Team")

    row_1_col1, row_1_col2, row_1_col3, row_1_col4 = st.columns(4)
    with row_1_col1:
        image = Image.open('streamlit_app/data/images/archit.jpeg')
        st.image(image, caption="Archit")
    with row_1_col2:
        image = Image.open('streamlit_app/data/images/male.jpg')
        st.image(image, caption="Bruno")
    with row_1_col3:
        image = Image.open('streamlit_app/data/images/male.jpg')
        st.image(image, caption="Shuai")
    with row_1_col4:
        image = Image.open('streamlit_app/data/images/male.jpg')
        st.image(image, caption="Zenan")