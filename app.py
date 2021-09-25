import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

######### Define functions ###########
# Move these to another file eventually
def display_results(df,baby_name):
    """
    Take a dataframe and name, generate chart of that name's history
    """
    
    # Get df filtered on that name
    name_df = df[df.name == baby_name]

    # Convert year to datetime, set as index
    # name_df['year'] = pd.to_datetime(name_df['year'], format="%Y")
    # name_df.set_index('year',inplace=True)

    # Plot chart
    # st.subheader("Number of {0}'s born by year".format(baby_name))
    # st.bar_chart(name_df[['count']])

    # Plot chart
    # st.subheader("Number of {0}s born by year".format(baby_name))
    # st.line_chart(name_df[['count']])

    # Create altair chart object
    st.subheader("Number of {0}s born by year".format(baby_name))
    c = alt.Chart(name_df).mark_line(interpolate='basis',strokeWidth=3).encode(
                alt.X('year(year):T', title='Year'),
                alt.Y('count', title='Count')
            )

    # Display the chart           
    st.altair_chart(c, use_container_width=True)


def display_multiple_line_charts(df):
    """
    Given df and the name of category column, generate line chart
    """
    st.line_chart(df[['count']])


def top_names_history(df,names_year,names_gender):
    """
    Take dataframe, gender and year, return df of complete history of top X names
    """
    
    # Get top names for given year
    top_names_list = get_top_names(df,names_year=names_year,names_gender=names_gender)['name'].unique()

    # Return df of data for all those top names
    history_df = df[df['name'].isin(top_names_list)]

    return history_df

def get_top_names(df,names_year=2020,names_gender='female',top_x=5):
    """
    Takes a dataframe of names with year, gender, rank. 
    Returns filtered dataframe for specified year, gender and top X names
    """    

    # Get the result of filtering df by year, gender, and top x
    top_df = df[(df.year == names_year) & (df.gender == names_gender) &  (df['rank'] <= top_x)][['rank','name','count']]
    # Set the rank as the index
    top_df.set_index('rank',inplace=True)
    # We want to also have rank as column to use
    top_df['rank'] = top_df.index

    return top_df

# Given a year, convert to decade for data grouping
def year_to_decade(year):
    decade = int(str(year)[:3]+'0')
    return decade

# Given a name, return probability of decades
def decade_probability(df,baby_name):
    name_df = df[df['name']==baby_name]
    name_df['decade'] = name_df.apply(lambda x: year_to_decade(x['year']),axis=1)
    decade_df = name_df.groupby(by=name_df['decade'])['count'].sum().reset_index(name='count')
    decade_df['prob'] = decade_df['count'] / decade_df['count'].sum()
    decade_df.sort_values('prob',ascending=False,inplace=True)
    return decade_df

def display_metrics(df,baby_name):
    """
    Take df and name and generate 3 metric cards in Streamlit
    """

    # Get copy of df for our name
    name_df2 = df[df.name == baby_name].copy(deep=True)
    # Sort by highest count & return year
    name_df2.sort_values(by='count',ascending=False,inplace=True)
    highest_year = name_df2.iloc[0].year
    highest_year_count = name_df2.iloc[0]['count']
    total_count = name_df2['count'].sum()

    # Get decade metric
    decade_df = decade_probability(df,baby_name)
    top_decade = int(decade_df.iloc[0].decade)
    top_prob = decade_df.iloc[0].prob
    
    # Display metrics side-by-side
    st.subheader('Interesting facts about {}'.format(baby_name))
    col1a, col2a, col3a = st.columns(3)
    col1a.metric("Most Popular Year",str(highest_year))
    col2a.metric("Total {}s".format(baby_name),human_format(total_count))
    col3a.metric("Most popular decade",str(top_decade)+"s")
    
    
    col1b, col2b, col3b = st.columns(3)
    col1b.metric("{0}s in {1}".format(baby_name,highest_year),human_format(highest_year_count))
    col3b.markdown("**{0:.0%}** of {1}s were born in the **{2}s**".format(top_prob,baby_name,top_decade))


def human_format(num):
    magnitude = 0
    while abs(num) >= 10000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'k', 'M', 'G', 'T', 'P'][magnitude])


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

    # Set top number
    top_x = 5

    # Select year
    year_select = st.slider(
    label="Year",
    min_value=1954,
    max_value=2020
    )

    # Get top 5 names for gender
    top_names_m = get_top_names(df=df,names_gender=gender_select,names_year=year_select,top_x=top_x)
    baby_name = top_names_m['name'].iloc[0]

    # Header for buttons
    st.subheader('Top {0} {1} names for {2}'.format(top_x,gender_select,year_select))

    # Create buttons for top names
    for name in top_names_m['name']:
        st.button(label=name,key=name)

    # Check if button clicked
    for name in top_names_m['name']:
        if st.session_state[name]:
            baby_name = name

    # display_results(df,baby_name)


    # MOVE THIS INTO A FUNCTION
    st.subheader("Number of {0}s born by year".format(baby_name))
    
    # Get history of top X names and plot
    history_df = top_names_history(df,year_select,gender_select)[['year','name','count']]

    # Create size column to highlight top name for current year
    history_df['size'] = np.where(history_df['name']==baby_name, 2, 1)

    # Get min/max for axis
    min_year = history_df['year'].min()
    max_year = history_df['year'].max()
    
    # Create altair chart object
    selection = alt.selection_multi(fields=['name'], bind='legend')
    c = alt.Chart(history_df).mark_line(interpolate='basis').encode(
                alt.X('year(year):T', title='Year', scale=alt.Scale(domain=(min_year-5, max_year))),
                alt.Y('count', title='Count'),
                alt.Color('name', title='Name', scale=alt.Scale(scheme='category10')), 
                alt.Size('size'),
                tooltip=['name','year(year):T','count'],
                opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
            ).add_selection(selection)

    # Add vertical line for selected year
    rule = alt.Chart(pd.DataFrame({
                    'year': [year_select],
                    'color': ['steelblue']
                })).mark_rule().encode(
                    x='year:T',
                    color=alt.Color('color:N', scale=None)
                )

    year_text = rule.mark_text(align='center', xOffset = 15, yOffset = 110)\
                .encode(text='year(year):T')


    # Display the chart           
    st.altair_chart(c + rule + year_text, use_container_width=True)

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
        # create kpi cards
        display_metrics(df,baby_name)
        # display results chart
        display_results(df,baby_name)
        
    else:
        st.error('{0} has not placed in the top 100 between 1954 and 2020.'.format(baby_name))

else:
    st.text('Choose already!')


##############
# Disclaimer #
##############
st.caption('**Data source:** Top 100 boys\' and girls\' names from 1954 to 2017 from [www.dia.govt.nz](www.dia.govt.nz)')