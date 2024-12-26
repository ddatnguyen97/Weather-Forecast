import streamlit as st
import pandas as pd

from data import *
from metrics import *
from charts import *
from filters import *

filter_7d_df = filter_7d_data(weather_df)

unique_wt_times_of_day = sorted(filter_7d_df['time_of_day'].unique())
unique_wt_month_day = sorted(filter_7d_df['month_day'].unique())

list_times_of_day_wt = ['All'] + unique_wt_times_of_day
list_month_day_wt = ['All'] + unique_wt_month_day

st.set_page_config(
    page_title="Weather Report",
    layout="wide",
    initial_sidebar_state="auto"
    )

st.markdown(
    """
    <style>
    .stApp {
        background-color: #2F3030;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image('../icon/hcmc-1.jpg', use_column_width=True)
st.title('HCM City Weather Report')
tab1, tab2, tab3, tab4 = st.tabs(['7 Days Report', 'Monthly Report', 'Air Quality', 'Future Prediction',])
with tab1:
    with st.container():
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            st.header('7 Days Weather Report')
        with col2:
            s_col1, s_col2, s_col3 = st.columns([0.2, 0.4, 0.4])
            with s_col2:
                wt_tod_select_box = st.selectbox('Times of Day', list_times_of_day_wt)
            with s_col3:
                wt_month_day_select_box = st.selectbox('Date (recent 7 days)', list_month_day_wt)
            with s_col1:
                image_map = {
                    'Day': '../icon/sun.png',
                    'Night': '../icon/full-moon.png',
                    'All': '../icon/day-and-night.png'
                }
                st.image(image_map.get(wt_tod_select_box, '../icon/day-and-night.png'), use_column_width=True)
                
    filter_7d_df = filter_column(filter_7d_df, 'time_of_day', wt_tod_select_box)
    filter_7d_df = filter_column(filter_7d_df, 'month_day', wt_month_day_select_box)         

    metrics = calculate_wt_metrics(filter_7d_df)

    avg_temp_by_day_hour = filter_7d_df.groupby(['month_day', 'time'])['temperature_2m'].mean().reset_index()
    sunshine_duration_by_day_hour = filter_7d_df.groupby(['month_day', 'time'])['sunshine_duration'].mean().reset_index()
    wind_data_by_day = filter_7d_df.groupby(['month_day', 'time'])[['wind_speed_10m', 'wind_gusts_10m']].mean().reset_index()
    rainfall_by_day = filter_7d_df.groupby(['month', 'day', 'month_day'])['precipitation'].mean().reset_index()

    temperature_chart = create_line_chart(avg_temp_by_day_hour,
                                           x='time', 
                                           y='temperature_2m', 
                                           title='Average Temperature by Hour', 
                                           color='month_day')
    temperature_chart.update_layout(legend_title_text='Day of Month')

    sunshine_duration_chart = create_area_chart(sunshine_duration_by_day_hour, 
                                                x='time', 
                                                y='sunshine_duration', 
                                                title='Average Sunshine Duration by Hour', 
                                                color='month_day')
    sunshine_duration_chart.update_layout(height=500, legend_title_text='Day of Month')

    wind_chart = create_line_chart(wind_data_by_day, 
                                   x='time', 
                                   y=['wind_speed_10m', 'wind_gusts_10m'], 
                                   title='Wind Speed and Gust by Hour', 
                                   color='month_day')
    wind_chart.update_layout(legend_title_text='Day of Month')

    rainfall_chart = create_bar_chart(rainfall_by_day, 
                                      x='day', 
                                      y='precipitation', 
                                      title='Rainfall by Day', 
                                      color='month_day')
    rainfall_chart.update_layout(legend_title_text='Day of Month')

    avg_uv_index_chart = create_gauge_chart(metrics['avg_uv_index'], 'AVG UV Index (mW/cm2)')
    avg_uv_index_chart.update_layout(height=240)
    avg_uv_clear_sky_chart = create_gauge_chart(metrics['avg_uv_clear_sky'], 'AVG UV Index CS (mW/cm2)')
    avg_uv_clear_sky_chart.update_layout(height=240)

    with st.container():
        st.subheader('Weather Metrics')
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                overall_data_card = st.metric(label='Overall Weather', 
                                            value=metrics['overall_weather'])

            with col2:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/humidity.png', use_column_width=True)
                with s_col2:
                    avg_humidity_indicator = st.metric(label='Average Humidity', 
                                                    value=metrics['avg_humidity_f'])

            with col3:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/binoculars.png', use_column_width=True)
                with s_col2:
                    max_visibility_indicator = st.metric(label='Max Visibility', 
                                                        value=metrics['max_visibility_f'])

            with col4:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/clouds.png', use_column_width=True)
                with s_col2:
                    avg_cloud_cover_indicator = st.metric(label='Average Cloud Cover',
                                                        value=metrics['avg_cloud_cover_f'])

        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:            
                comfort_index_card = st.metric(label='Comfort Index',
                                            value=metrics['comfort_index'])

            with col2:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/drop.png', use_column_width=True)
                with s_col2:
                    dew_point_indicator = st.metric(label='Dew Point',
                                                    value=metrics['avg_dew_point'])

            with col3:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/evaporation.png', use_column_width=True)
                with s_col2:
                    evaporation_indicator = st.metric(label='Average Evaporation',
                                                    value=metrics['avg_evapotranspiration'])

            with col4:
                s_col1, s_col2 = st.columns([0.2, 0.8])
                with s_col1:
                    st.image('../icon/water-vapor.png', use_column_width=True)
                with s_col2:
                    vapor_press_deficit_indicator = st.metric(label='Average Vapor Pressure Deficit', 
                                                            value=metrics['avg_vapour_pressure_deficit'])
    
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

filter_5year_df = filter_5y_data(weather_df)
filter_5year_df['year'] = filter_5year_df['year'].astype(str)

unique_wt_year = sorted(filter_5year_df['year'].unique())
list_year_wt = ['All'] + unique_wt_year

with tab2:
    with st.container():
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.header('Monthly Weather Report')
        with col2:
            year_select_box = st.selectbox('Year', list_year_wt)
    filter_wt_year_df = filter_column(filter_5year_df, 'year', year_select_box)
    
    if year_select_box != 'All':
        avg_temp_by_month = filter_wt_year_df.groupby(['month', 'year', 'year_month'])['temperature_2m'].mean().reset_index()
        max_temp_by_month = filter_wt_year_df.groupby(['month', 'year', 'year_month'])['temperature_2m'].max().reset_index()
        min_temp_by_month = filter_wt_year_df.groupby(['month', 'year', 'year_month'])['temperature_2m'].min().reset_index()
        avg_rainfall_by_month = filter_wt_year_df.groupby(['year', 'month','year_month'])[['precipitation']].mean().reset_index()

        temp_metrics_by_month = create_combine_chart([avg_temp_by_month, max_temp_by_month, min_temp_by_month],
                                                    ['Average Temp', 'Max Temp', 'Min Temp'],
                                                    'month',
                                                    ['temperature_2m', 'temperature_2m', 'temperature_2m'],
                                                    'Temperature Metrics by Month',
                                                    'Month',
                                                    'Temperature (°C)',
                                                    ['bar', 'bar', 'bar'],
                                                    colors=['#1f77b4', '#ff7f0e', '#2ca02c'])

        rainfall_by_month = create_bar_chart(avg_rainfall_by_month,
                                                x='month',
                                                y='precipitation',
                                                title='Average Rainfall by Month',
                                                color='year')
        rainfall_by_month.update_layout(barmode='group')
        
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            st.subheader('Temperature Reports')
            st.plotly_chart(temp_metrics_by_month, use_container_width=True)
        with col2:
            st.subheader('Rainfall Reports')
            st.plotly_chart(rainfall_by_month, use_container_width=True)

    else:
        avg_temp_by_year = filter_wt_year_df.groupby(['year'])['temperature_2m'].mean().reset_index()
        avg_rainfall_by_year = filter_wt_year_df.groupby(['year'])['precipitation'].mean().reset_index()
        
        temp_metrics_by_year = create_bar_chart(avg_temp_by_year,
                                                x='year',
                                                y='temperature_2m',
                                                title='Average Temperature by Year',
                                                color='year')
        temp_metrics_by_year.update_layout(xaxis=dict(type='category'))

        rainfall_by_year = create_bar_chart(avg_rainfall_by_year,
                                            x='year',
                                            y='precipitation',
                                            title='Average Rainfall by Year',
                                            color='year')
        rainfall_by_year.update_layout(xaxis=dict(type='category'))
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            st.subheader('Temperature Reports')
            st.plotly_chart(temp_metrics_by_year, use_container_width=True)
        with col2:
            st.subheader('Rainfall Reports')
            st.plotly_chart(rainfall_by_year, use_container_width=True)

# aq_7d_df = filter_7d_data(aq_df)
# list_times_of_day_aq = ['All'] + sorted(list(aq_7d_df['time'].unique()))
# list_month_day_aq = ['All'] + sorted(list(aq_7d_df['month_day'].unique()))

with tab3:
    with st.container():
        # st.write('Coming soon ...')
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.header('Air Quality Report')
        # with col2:
            # aq_times_of_day = st.selectbox('Times of day', list_times_of_day_aq)
            
with tab4:
    with st.container():
        st.header('Future Prediction Report')
        st.write('Coming soon ...')
