import streamlit as st
import pandas as pd

from data import *
from metrics import *
from charts import *

filter_7d_df = filter_7d_data(weather_df)

list_times_of_day = ['All'] + sorted(list(filter_7d_df['time_of_day'].unique()))
list_month_day = ['All'] + sorted(list(filter_7d_df['month_day'].unique()))

st.set_page_config(
    page_title="Weather Report",
    layout="wide",
    initial_sidebar_state="auto"
    )

st.markdown(
    """
    <style>
    .stApp {
        background-color: #2F3030;  /* Change this to your desired background color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image('../icon/hcmc-1.jpg', use_column_width=True)
st.title('HCM City Weather Dashboard')
tab1, tab2 = st.tabs(['7 Days Report', 'Future Prediction'])
with tab1:
    with st.container():
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            st.header('7 Days Weather Report')
        with col2:
            s_col1, s_col2, s_col3 = st.columns([0.2, 0.4, 0.4])
            with s_col2:
                tod_select_box = st.selectbox('Times of Day', list_times_of_day)
            with s_col3:
                month_day_select_box = st.selectbox('Date (recent 7 days)', list_month_day)
            with s_col1:
                if tod_select_box == 'Day':
                    st.image('../icon/sun.png', use_column_width=True)
                elif tod_select_box == 'Night':
                    st.image('../icon/full-moon.png', use_column_width=True)
                else:
                    st.image('../icon/day-and-night.png', use_column_width=True)
                
    if tod_select_box != 'All':
        filter_7d_df = filter_7d_df[filter_7d_df['time_of_day'] == tod_select_box]   

    if month_day_select_box != 'All':
        filter_7d_df = filter_7d_df[filter_7d_df['month_day'] == month_day_select_box]         

    metrics = calculate_metrics(filter_7d_df)

    avg_temp_by_day_hour = filter_7d_df.groupby(['month_day', 'time'])['temperature_2m'].mean().reset_index()
    sunshine_duration_by_day_hour = filter_7d_df.groupby(['month_day', 'time'])['sunshine_duration'].mean().reset_index()
    wind_data_by_day = filter_7d_df.groupby(['month_day', 'time'])[['wind_speed_80m', 'wind_gusts_10m']].mean().reset_index()
    rainfall_data_by_day = filter_7d_df.groupby(['month_day', 'time'])[['precipitation', 'rain', 'showers']].mean().reset_index()

    temperature_chart = create_line_chart(avg_temp_by_day_hour, x='time', y='temperature_2m', title='Average Temperature by Hour', color='month_day')
    sunshine_duration_chart = create_area_chart(sunshine_duration_by_day_hour, x='time', y='sunshine_duration', title='Average Sunshine Duration by Hour', color='month_day')
    sunshine_duration_chart.update_layout(height=500)
    wind_chart = create_line_chart(wind_data_by_day, x='time', y=['wind_speed_80m', 'wind_gusts_10m'], title='Wind Speed and Gust by Hour', color='month_day')
    rainfall_chart = create_bar_chart(rainfall_data_by_day, x='time', y=['precipitation', 'rain', 'showers'], title='Rainfall by Hour', color='month_day')

    avg_uv_index_chart = create_gauge_chart(metrics['avg_uv_index'], 'AVG UV Index (mW/cm2)')
    avg_uv_index_chart.update_layout(height=240)
    avg_uv_clear_sky_chart = create_gauge_chart(metrics['avg_uv_clear_sky'], 'AVG UV Index CS (mW/cm2)')
    avg_uv_clear_sky_chart.update_layout(height=240)
    
    with st.container():
        st.subheader('Weather Metrics')
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                overall_data_card = st.metric(label='Overall Weather', value=metrics['overall_weather'])

            with col2:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/humidity.png', use_column_width=True)
                with s_col2:
                    avg_humidity_indicator = st.metric(label='Average Humidity', value=metrics['avg_humidity_f'])

            with col3:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/binoculars.png', use_column_width=True)
                with s_col2:
                    max_visibility_indicator = st.metric(label='Max Visibility', value=metrics['max_visibility_f'])

            with col4:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/clouds.png', use_column_width=True)
                with s_col2:
                    avg_cloud_cover_indicator = st.metric(label='Average Cloud Cover', value=metrics['avg_cloud_cover_f'])

        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:            
                comfort_index_card = st.metric(label='Comfort Index', value=metrics['comfort_index'])

            with col2:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/drop.png', use_column_width=True)
                with s_col2:
                    dew_point_indicator = st.metric(label='Dew Point', value=metrics['avg_dew_point'])

            with col3:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/evaporation.png', use_column_width=True)
                with s_col2:
                    evaporation_indicator = st.metric(label='Average Evaporation', value=metrics['avg_evapotranspiration'])

            with col4:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/water-vapor.png', use_column_width=True)
                with s_col2:
                    vapor_press_deficit_indicator = st.metric(label='Average Vapor Pressure Deficit', value=metrics['avg_vapour_pressure_deficit'])
    
    st.divider()
    with st.container():
        st.subheader('Temperature Reports')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            s_col1, s_col2, = st.columns([0.2, 0.8])
            with s_col1:
                st.image('../icon/high-temperature.png', use_column_width=True)
            with s_col2:
                st.metric(label='Max Temp', value=metrics['max_temp_f'])

        with col2:     
            s_col1, s_col2, = st.columns([0.2, 0.8])
            with s_col1:
                st.image('../icon/low-temperature.png', use_column_width=True)
            with s_col2:
                st.metric(label='Min Temp', value=metrics['min_temp_f'])
                
        with col3:    
            s_col1, s_col2, = st.columns([0.2, 0.8])
            with s_col1:
                st.image('../icon/thermometer.png', use_column_width=True)
            with s_col2:
                st.metric(label='Avg Temp', value=metrics['avg_temp_f'])
        
        st.plotly_chart(temperature_chart, use_container_width=True)
    
    st.divider()
    with st.container():
        st.subheader('Sunshine Duration and UV Index Reports')
        col1, col2 = st.columns([0.2, 0.8])
        with col1:
            st.plotly_chart(avg_uv_index_chart, use_container_width=True)
            st.plotly_chart(avg_uv_clear_sky_chart, use_container_width=True)
        with col2:
            st.plotly_chart(sunshine_duration_chart, use_container_width=True)
    
    st.divider()
    with st.container():
        st.subheader('Wind Reports')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            s_col1, s_col2 = st.columns([0.2, 0.8])
            with s_col1:
                st.image('../icon/compass.png', use_column_width=True)
            with s_col2:
                st.metric(label='Overall Wind Direction', value=metrics['overall_wind_direction'])
        with col2:
            s_col1, s_col2 = st.columns([0.2, 0.8])
            with s_col1:
                st.image('../icon/wind.png', use_column_width=True)
            with s_col2:
                st.metric(label='Average Wind Speed', value=metrics['wind_speed_f'])
        with col3:
            s_col1, s_col2 = st.columns([0.2, 0.8])
            with s_col1:
                st.image('../icon/gust.png', use_column_width=True)
            with s_col2:    
                st.metric(label='Average Wind Gust', value=metrics['wind_gust_f'])

        st.plotly_chart(wind_chart, use_container_width=True)

    st.divider()
    with st.container():
        st.subheader('Rainfall Reports')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            s_col1, s_col2 = st.columns([0.2, 0.8])
            with s_col1:
                st.image('../icon/rainfall.png', use_column_width=True)
            with s_col2:
                st.metric(label='Average Precipitation', value=metrics['avg_precipitation'])
        with col2:
            s_col1, s_col2 = st.columns([0.2, 0.8])
            with s_col1:
                st.image('../icon/raining.png', use_column_width=True)
            with s_col2:
                st.metric(label='Average Rain', value=metrics['avg_rain'])
        with col3:
            s_col1, s_col2 = st.columns([0.2, 0.8])
            with s_col1:
                st.image('../icon/heavy-rain.png', use_column_width=True)
            with s_col2:    
                st.metric(label='Average Showers', value=metrics['avg_showers'])
        
        st.plotly_chart(rainfall_chart, use_container_width=True)
        


