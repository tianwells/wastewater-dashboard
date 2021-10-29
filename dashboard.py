#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 18:34:26 2021

@author: tianwells
"""

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Wastewater Testing Initiative', layout="wide")
st.header('Wastewater Testing Initiative')
st.subheader('Columbia University')

# --- LOAD DATAFRAME
excel_file = 'Watewater viral concentraiton.xlsx'
sheet_name = 'by location'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name, usecols='A, B, Z, AG',
                   header=1)

df.dropna(inplace=True)

# --- STREAMLIT SELECTION
og_location = df['Location'].unique().tolist()
sample_dates = df['Sample date'].unique().tolist()

location = []

for element in og_location:
    location.append(element.strip())

location_selection = st.selectbox("Residence Hall:", location)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = df.loc[df['Location'].str.contains(location_selection)]
number_of_result = mask.shape[0]
mask_new = mask.sort_values('Sample date')
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped1 = mask_new["Average             (copies/mL raw sample)"]
df_grouped1 = df_grouped1.reset_index()

df_grouped2 = mask_new["Average             (copies/mL raw sample).1"]
df_grouped2 = df_grouped2.reset_index()

# --- PLOT LINE CHART

bar_chart = px.bar(mask_new,
                   x='Sample date',
                   y=["Average             (copies/mL raw sample)", 
                      "Average             (copies/mL raw sample).1"],
                   log_y = True, width = 1000,
                   labels=dict(value="Marker Concentration (copies/mL)"),
                   title = "Wastewater Viral Concentration",
                   barmode='group', template='plotly_white')

newnames = {'Average             (copies/mL raw sample)':'Viral Marker 1', 
            'Average             (copies/mL raw sample).1': 'Viral Marker 2'}
bar_chart.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )

bar_chart.update_yaxes(showgrid=True)
bar_chart.update_xaxes(nticks=number_of_result)



st.plotly_chart(bar_chart, use_container_width=True)
