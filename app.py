import streamlit as st
import numpy as np
import pandas as pd

## Run this code to deploy app:
# streamlit run app.py

## Set up git repo for it as well

st.title('NZ Baby Names')

# Define dataframe
df = pd.read_csv('nz_baby_names.csv').sort_values(by=['year','rank'])

# Set specific name
st.text_input("Enter baby name:", key="name")
baby_name = st.session_state.name.capitalize()

# Get df filtered on that name
name_df = df[df.name == baby_name][['year','count']]
# Convert year to datetime, set as index
name_df['year'] = pd.to_datetime(name_df['year'], format="%Y")
name_df.set_index('year',inplace=True)

# Write boring data table
# st.write("{0} Data".format(baby_name))
# st.write(name_df)

# Plot line chart
st.write("{0} Chart".format(baby_name))
st.bar_chart(name_df)


# Disclaimer
st.text('Note: data is only available where the name placed in the top 100 for girl or boy names between 1954 and 2020.')