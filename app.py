import streamlit as st
import numpy as np
import pandas as pd

## Run this code to deploy app:
# streamlit run baby_names_app.py

## Set up git repo for it as well

st.title('NZ Baby Names from 1954-2020')

# Define dataframe
df = pd.read_csv('nz_baby_names.csv').sort_values(by=['year','rank'])

# Specific name
specific_name = 'John'
specific_name_df = df[df.name == 'John'][['year','count']]

st.write("{0} Data".format(specific_name))
st.write(specific_name)

st.write("{0} Chart".format(specific_name))
st.line_chart(specific_name)