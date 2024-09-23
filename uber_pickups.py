# Importing libraries
import streamlit as st
import pandas as pd
import numpy as np

# Writing the Streamlit app code 

# Specifying the title of the app
st.title("Uber Pickups Analysis")

# Fetching the Uber dataset for pickups and drop-offs in New York City
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data # to avoid re-running the data loading process if the inputs haven’t changed.
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Testing the function and reviewing the output
# Creating a text element and letting the reader know the data is loading.
data_load_state = st.text('Loading data...')

# Loading 10,000 rows of data into the dataframe
data = load_data(10000)

# Notifying the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

# Overview about what the app does so users can understand
st.write("""
### What is this app?
This app visualizes Uber pickup data in New York City 
to analyze the busiest times and days for Uber pickups 
and where they are most concentrated in the city.
""")

# Inspecting the raw data in an interactive table
st.write("""
### Take a look at the raw data by clicking on the checkbox.
""")
# Adding a checkbox to show/hide the raw data table
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Drawing a histogram of Uber pickups by hour
# Adding a subheader for the histogram
st.subheader('Number of pickups by hour')

# Generating the values of the histogram
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]

# Drawing the histogram
st.bar_chart(hist_values)

# Insights for the histogram
st.write("""
#### Insights:
The above histogram presents the distribution of Uber pickups based on the time.
The busiest time for Uber pickups is around **5 P.M.**. 
This could be due to the end of the workday when people are likely heading home. 
There is a moderate activity throughout the day. 
Afternoon hours are marked by higher activity compared to morning hours.
""")

# Plotting Uber pickup data on a map

# Adding a slider for dynamically filtering the Uber pickups by hour
# Adding a slider for hour selection
hour_to_filter = st.slider('Select hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h

# Filtering for pickups at the selected hour
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

# Insights for the map
st.write(f"""
#### Insights:
The above map visualizes Uber pickups in New York City at various times of the day. 
The pickups seem to be are heavily concentrated in areas like Manhattan.
Thus there is a high demand for rides around this area, especially during rush hour at 17:00. 
""")

# Filtering the data for the busiest pickup time at 17:00
hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)