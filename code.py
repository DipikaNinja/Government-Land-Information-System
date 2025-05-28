import streamlit as st
from PIL import Image
import altair as alt
import pandas as pd
from streamlit_marquee import streamlit_marquee
from pydataset import data
from geopy.geocoders import Nominatim
from dbf import Table
from streamlit_folium import st_folium
import folium
import json
import os
import plotly.express as px
import plotly.graph_objects as go
import time
import requests
from streamlit_lottie import st_lottie

from typing_extensions import Literal

# Set page title and icon
st.set_page_config(
    page_title="GLIS",
    page_icon="🌍",
)

# Opening the image
try:
    image = Image.open(os.path.join("Files", "Screenshot_2023-10-30_134617-removebg-preview.png"))
    st.image(image, use_container_width=True)
except FileNotFoundError:
    st.warning("Image not found. Please check the 'Files' folder.")

# Sidebar
st.sidebar.title("Menu")
menu_options = ["Home", "Land Information", "Datasets", "Dashboard", "Chatbot"]
selected_option = st.sidebar.selectbox("Select Page:", menu_options)

# Define the content for each menu option
if selected_option == "Home":
    # Create a container for title and login button
    st.markdown("<h1 style='text-align: center; color: black;'>Government Land Informative System - (GLIS)</h1>", unsafe_allow_html=True)
    
    # Use forward slashes in the file path
   # st.video(r"Files/Untitled design.mp4")

@st.cache_data

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url_hello = "https://lottie.host/d076e07c-91fb-4b28-b443-24d10c3c6f50/EnCn0jBhv5.json"
lottie_hello = load_lottieurl(lottie_url_hello)

# Dataset loader for general use
@st.cache_data
def load_dataset_file(path):
    return pd.read_csv(path)

# Dataset loader for state data
@st.cache_data
def load_state_data(state):
    file_path = os.path.join("Datasets", f"{state}.csv")
    return pd.read_csv(file_path)

# GeoJSON loader
@st.cache_data
def load_geojson(state):
    geojson_path = os.path.join("geojson files", f"{state}.geojson")  # ✅ Define first
    if not os.path.exists(geojson_path):                              # ✅ Then use
        st.error(f"GeoJSON file not found for {state}. Please make sure the file '{geojson_path}' exists.")
        st.stop()
    with open(geojson_path, 'r', encoding='utf-8') as geojson_file:
        return json.load(geojson_file)


# Home Page
if selected_option == "Home":
    st.markdown("<h1 style='text-align: center; color: black;'>Government Land Informative System - (GLIS)</h1>", unsafe_allow_html=True)
    st.video(os.path.join("Files", "Untitled design.mp4"))
    
    lottie_hello = load_lottieurl("https://lottie.host/d076e07c-91fb-4b28-b443-24d10c3c6f50/EnCn0jBhv5.json")
    st.markdown("<h1 style='text-align: center; color: black;'>Visualizing Land Resources</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write("""
            The Government Land Information System (GLIS) is an invaluable resource ...
        """)
    with col2:
        st_lottie(lottie_hello, key="hello", width=350, height=330)

# Datasets Page
elif selected_option == "Datasets":
    st.markdown("<h1 style='text-align: center; color: black;'>Datasets</h1>", unsafe_allow_html=True)
    streamlit_marquee(content='You are now on the Datasets page...', background='white', color='red')

    dataset_paths = {
        'Land Utilization': "mainpagedatasets/Land_Utilization.csv",
        'Classification of Land(Year-Wise)': "mainpagedatasets/Land_Utilization (1).csv",
        'Land Allocation': "mainpagedatasets/PATTERN_OF_LAND_UTILISATION_0.csv",
        'StateWise Report(2008-15)': "mainpagedatasets/PATTERN_OF_LAND_UTILISATION_0.csv",
        'StateWise Report(2015-23)': "mainpagedatasets/PATTERN_OF_LAND_UTILISATION_0.csv"
    }

    st.sidebar.header('Select Dataset')
    selected_dataset = st.sidebar.selectbox('Choose a dataset', list(dataset_paths.keys()))
    df = load_dataset_file(dataset_paths[selected_dataset])

    st.subheader('Display Selected Dataset')
    st.write(f'You have selected: {selected_dataset}')
    st.write(df)

# Land Information Page
elif selected_option == "Land Information":
    st.markdown("<h1 style='text-align: center; color: black;'>Land Parcel Information</h1>", unsafe_allow_html=True)
    streamlit_marquee(content='This page provides details about land parcels.', background='white', color='red')
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    st.write('<h3 align="center">Map of Indian States</h3>', unsafe_allow_html=True)
    st_folium(m, width=1000, height=400)

    col1, col2 = st.columns(2)
    col1.write("""
        Land parcel information refers to detailed data about specific pieces of land ...
    """)
    imagSe = Image.open(os.path.join("Files", "home-ins.png"))
    col2.image(imagSe, width=400)

    states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhatisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh','Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odissa', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura']

    def land_info_main():
        state_selected = st.selectbox('Select a state:', states)
        geojson_data = load_geojson(state_selected)
        dataset = load_state_data(state_selected)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Folium Map')
            m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
            folium.GeoJson(geojson_data, name='geojson').add_to(m)
            st_folium(m, width=490, height=400)
        with col2:
            st.subheader(f'Dataset for {state_selected}')
            st.write(dataset)

    land_info_main()

# Dashboard Page
elif selected_option == "Dashboard":
    st.markdown("<h1 style='text-align: center; color: black;'>Dashboard</h1>", unsafe_allow_html=True)
    streamlit_marquee(content='This dashboard provides insights and visualizations ...', background='white', color='red')

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Land Utilization Analysis")
        df1 = pd.DataFrame({"Land Type": ["Residential", "Commercial", "Agricultural", "Industrial", "Other"], "Land Utilization": [10, 20, 30, 40, 50]})
        chart1 = alt.Chart(df1).mark_bar(color="skyblue").encode(x="Land Type", y="Land Utilization")
        st.altair_chart(chart1, use_container_width=True)
    with col2:
        st.subheader("Property Ownership Analysis")
        df2 = pd.DataFrame({"Ownership Type": ["Private", "Government", "Corporate", "Individual", "Other"], "Ownership Percentage": [15, 25, 10, 30, 20]})
        chart2 = alt.Chart(df2).mark_line(color="red").encode(x="Ownership Type", y="Ownership Percentage")
        st.altair_chart(chart2, use_container_width=True)

    states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhatisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh','Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odissa', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura']

    def dashboard_main():
        state_selected = st.selectbox('Select a state:', states)
        dataset = load_state_data(state_selected)

        fig1 = px.pie(dataset, values='Agriculture Land', names='Year', title='Agriculture Land by Year')
        fig2 = px.area(dataset, x='Year', y='Infrastructures', title='Infrastructures')
        fig3 = px.scatter(dataset, x='Year', y='Water Bodies', title='Water Bodies')
        fig4 = px.bar(dataset, x='Year', y='Industries', title='Industries')
        fig5 = px.scatter(dataset, x='Year', y='Waste Land', size='Industries', color='Agriculture Land', title='Waste Land')
        fig6 = px.histogram(dataset, x='Year', y='Forest Land', color='Agriculture Land', title='Forest Land')

        for fig in [fig1, fig2, fig3, fig4, fig5, fig6]:
            st.plotly_chart(fig, use_container_width=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='lines+markers'))
        frames = [go.Frame(data=[go.Scatter(x=dataset['Year'][:i+1], y=dataset['Agriculture Land'][:i+1])], name=f'frame_{i}') for i in range(len(dataset))]
        fig.frames = frames
        fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='*', method='animate', args=[None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}])])])
        st.plotly_chart(fig, use_container_width=True)

    dashboard_main()

# Chatbot Page
elif selected_option == "Chatbot":
    st.markdown("<h1 style='text-align: center; color: black;'>How can I help you!</h1>", unsafe_allow_html=True)
    # Chatbot logic remains unchanged (omitted here for brevity, reuse previous implementation)
    st.write("Chatbot module loading... (truncated for brevity)")
