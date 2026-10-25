import numpy as np
import pandas as pd
import streamlit as st
 
st.title("Uber pickups in NYC")
 
DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)
 
 
@st.cache_data
def load_data(nrows):
    # Cached: Streamlit re-runs this script on every interaction,
    # so without the cache the file would download again each time.
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename(lambda x: str(x).lower(), axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
 
 
data_load_state = st.text("Loading data...")
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")
 
# Checkbox: show or hide the raw table
if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)
 
# Histogram: pickups per hour of the day
st.subheader("Number of pickups by hour")
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24)
)[0]
st.bar_chart(hist_values)
 
# Slider: choose an hour (0-23) and map only that hour's pickups
hour_to_filter = st.slider("hour", 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
 
st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)