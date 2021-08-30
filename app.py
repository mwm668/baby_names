import streamlit as st
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

######### Define function ###########
# Move these to another file eventually
def display_results(baby_name):
    
    # What happens if we don't find that name?
    
    # Get df filtered on that name
    name_df = df[df.name == baby_name]
    # Convert year to datetime, set as index
    name_df['year'] = pd.to_datetime(name_df['year'], format="%Y")
    name_df.set_index('year',inplace=True)

    # Plot chart
    st.subheader("Number of {0}'s born by year".format(baby_name))
    st.bar_chart(name_df[['count']])

    # Plot chart
    # st.subheader("Rank of {0} by year".format(baby_name))
    # st.line_chart(name_df[['rank']])

# Set title
st.title('Baby Names of NZ')
st.text('Select to search by name or year:')

# Define dataframe
df = pd.read_csv('nz_baby_names.csv').sort_values(by=['year','rank'])

####################
# Top names viewer #
####################

# Define columns for widget layout
# try except because different versions of streamlit being annoying
try:
    left_column, right_column = st.columns(2)
except:
    left_column, right_column = st.beta_columns(2)

# Select top-level of analysis
year_or_name_select = left_column.radio('Search by',['Year','Name'])
year_or_name_select = year_or_name_select.lower()

# Select gender of name
gender_select = right_column.radio('Gender',['Female','Male'])
gender_select = gender_select.lower()

##### CONTROL FLOW ########
if year_or_name_select == 'year':
    #########################
    # Specfic YEAR analysis #
    #########################

    # Select year
    year_select = st.slider(
    label="Year",
    min_value=1954,
    max_value=2020
    )

    # Write top names for year_select
    top_df = df[(df.year == year_select) & (df.gender == gender_select) &  (df['rank'] <= 10)][['rank','name','count']]
    top_df.set_index('rank',inplace=True)
    top_df['rank'] = top_df.index

    if st.checkbox('Show top names'):
        left_column.write("{0} names for {1}".format(gender_select.capitalize(),year_select))
        left_column.write(top_df)
        baby_name = right_column.selectbox(options=top_df['name'], label='Select other top name')
        display_results(baby_name)
    else:
        # Use top name as default for specific name chart
        baby_name = top_df.loc[1]['name']  
        display_results(baby_name)

elif year_or_name_select == 'name':
    #########################
    # Specfic NAME analysis #
    #########################

    # Set specific name
    baby_name = 'John'
    st.text_input("Enter baby name:", value=baby_name,key="name")
    baby_name = st.session_state.name.capitalize()

    # display results
    display_results(baby_name)

else:
    st.text('Choose already!')


##############
# Disclaimer #
##############
st.markdown('**Note:** data is only available where the name placed in the top 100 for girl or boy names between 1954 and 2020.')