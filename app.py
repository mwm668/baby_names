import streamlit as st
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

######### Define functions ###########
# Move these to another file eventually
def display_results(baby_name):
    
    # Get df filtered on that name
    name_df = df[df.name == baby_name]

    # Convert year to datetime, set as index
    name_df['year'] = pd.to_datetime(name_df['year'], format="%Y")
    name_df.set_index('year',inplace=True)

    # Plot chart
    # st.subheader("Number of {0}'s born by year".format(baby_name))
    # st.bar_chart(name_df[['count']])

    # Plot chart
    st.subheader("Number of {0}'s born by year".format(baby_name))
    st.area_chart(name_df[['count']])

    # st.balloons()

def get_top_names(df,names_year=2020,names_gender='female',top_x=10):
    """
    Takes a dataframe of names with year, gender, rank. 
    Returns filtered dataframe for specified year, name and top X
    """    

    # Get the result of filtering df by year, gender, and top x
    top_df = df[(df.year == names_year) & (df.gender == names_gender) &  (df['rank'] <= top_x)][['rank','name','count']]
    # Set the rank as the index
    top_df.set_index('rank',inplace=True)
    # We want to also have rank as column to use
    top_df['rank'] = top_df.index

    return top_df


# Set title
st.title('👶 Baby Names of NZ 👶')
st.subheader('Search by name or year:')

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
year_or_name_select = left_column.radio('',['Year','Name'])
year_or_name_select = year_or_name_select.lower()

# Select gender of name
gender_select = right_column.radio('',['Female','Male'])
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

    # Get top 5 names for gender
    top_names_m = get_top_names(df=df,names_gender=gender_select,names_year=year_select,top_x=5)
    baby_name = top_names_m['name'].iloc[0]

    # Header for buttons
    st.subheader('Top 5 {0} names for {1}'.format(gender_select,year_select))

    # Create buttons for top names
    for name in top_names_m['name']:
        st.button(label=name,key=name)

    # Check if button clicked
    for name in top_names_m['name']:
        if st.session_state[name]:
            baby_name = name

    display_results(baby_name)
    
    # if st.checkbox('Show top names'):
    #     left_column.write("{0} names for {1}".format(gender_select.capitalize(),year_select))
    #     left_column.write(top_df)
    #     baby_name = right_column.selectbox(options=top_df['name'], label='Select other top name')
    #     display_results(baby_name)
    # else:
    #     # Use top name as default for specific name chart
    #     baby_name = top_df.loc[1]['name']  
    #     display_results(baby_name)

elif year_or_name_select == 'name':
    #########################
    # Specfic NAME analysis #
    #########################

    # Set default name for use in input box
    top_names_m = get_top_names(df=df,names_gender=gender_select,top_x=5)
    baby_name = top_names_m['name'].iloc[0]

    # Set specific name in input box
    st.text_input("Enter baby name:", value=baby_name,key="name_input")
    baby_name = st.session_state['name_input'].capitalize()

    # Check that name is in list
    if len(df[df['name']==baby_name]) > 0:
        # display results
        display_results(baby_name)
    else:
        st.error('{0} has not placed in the top 100 between 1954 and 2020.'.format(baby_name))

else:
    st.text('Choose already!')


##############
# Disclaimer #
##############
st.caption('**Data source:** Top 100 boys\' and girls\' names from 1954 to 2017 from [www.dia.govt.nz](www.dia.govt.nz)')