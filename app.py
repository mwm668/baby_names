import streamlit as st
import numpy as np
import pandas as pd

# Set title
st.title('NZ Baby Names')

# Define dataframe
df = pd.read_csv('nz_baby_names.csv').sort_values(by=['year','rank'])

####################
# Top names viewer #
####################

# Define columns for widget layout
left_column, right_column = st.columns(2)

# Select gender of name
gender_select = left_column.radio('Gender',['Female','Male'])
gender_select = gender_select.lower()

# Select year
year_select = right_column.slider(
    label="Year",
    min_value=1954,
    max_value=2020
    )

# Write top names for year_select
top_df = df[(df.year == year_select) & (df.gender == gender_select) &  (df['rank'] <= 10)][['rank','name','count']]
top_df.set_index('rank',inplace=True)
top_df['rank'] = top_df.index

if st.checkbox('Show top names'):
    st.write("{0} names for {1}".format(gender_select.capitalize(),year_select))
    st.write(top_df)

# Use top name as default for specific name chart
baby_name = top_df.loc[1]['name']

#########################
# Specfic name analysis #
#########################

# Set specific name
st.text_input("Enter baby name:", value=baby_name,key="name")
baby_name = st.session_state.name.capitalize()

# Get df filtered on that name
name_df = df[df.name == baby_name]
# Convert year to datetime, set as index
name_df['year'] = pd.to_datetime(name_df['year'], format="%Y")
name_df.set_index('year',inplace=True)

# Plot chart
st.subheader("Number of {0}'s born by year".format(baby_name))
st.bar_chart(name_df[['count']])

# Plot chart
st.subheader("Rank of {0} by year".format(baby_name))
st.line_chart(name_df[['rank']])

##############
# Disclaimer #
##############
st.markdown('**Note:** data is only available where the name placed in the top 100 for girl or boy names between 1954 and 2020.')