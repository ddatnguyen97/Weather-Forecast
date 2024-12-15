import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import logging

load_dotenv()
db_config = {
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'db_name': os.getenv('DB_NAME')
}
connection_string = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db_name']}"

def fetch_data(query):
    try:
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            result = connection.execute(query)
            values = result.fetchall()
            columns = result.keys()
            return columns, values
    
    except Exception as e:
        logging.error(f"Error fetching weather data: {str(e)}")
        raise

weather_query = text("""SELECT * FROM hcm_weather""")
w_columns, w_values = fetch_data(weather_query)
weather_df = pd.DataFrame(w_values, columns=w_columns)

date_query = text("""SELECT * FROM dim_date""")
d_columns, d_values = fetch_data(date_query)
date_df = pd.DataFrame(d_values, columns=d_columns)
weather_df = weather_df.merge(date_df, left_on='date_id', right_on='id', suffixes=('_w', '_date'))

time_query = text("""SELECT * FROM dim_time""")
t_columns, t_values = fetch_data(time_query)
time_df = pd.DataFrame(t_values, columns=t_columns)
weather_df = weather_df.merge(time_df, left_on='time_id', right_on='id', suffixes=('', '_time'))

times_of_day_query = text("""SELECT * FROM times_of_day""")
tod_columns, tod_values = fetch_data(times_of_day_query)
times_of_day_df = pd.DataFrame(tod_values, columns=tod_columns)
weather_df = weather_df.merge(times_of_day_df, left_on='is_day', right_on='id', suffixes=('', '_tod'))

weather_code_query = text("""SELECT * FROM weather_code""")
wc_columns, wc_values = fetch_data(weather_code_query)
weather_code_df = pd.DataFrame(wc_values, columns=wc_columns)
weather_df = weather_df.merge(weather_code_df, left_on='weather_code', right_on='id', suffixes=('', '_wc'))

weather_df.drop(columns=[
            'id_w',
            'date_id',
            'time_id',
            'is_day',
            'weather_code',
            'id_date',
            'id',
            'id_tod',
            'id_wc',
            ], inplace=True)

weather_df['date'] = pd.to_datetime(weather_df['date'])

weather_df['month_date'] = weather_df['date'].dt.strftime('%m-%d')
weather_df.rename(columns={'name': 'times of day'}, inplace=True)
max_date = weather_df['date'].max()
seven_days_ago = max_date - pd.DateOffset(days=6)

seven_days_df = weather_df[weather_df['date'] >= seven_days_ago]

st.set_page_config(
    page_title="Weather Report",
    # page_icon="🏂",
    layout="wide",
    initial_sidebar_state="auto"
    )
# st.dataframe(seven_days_df.head())
# # st.write(seven_days_df.columns)
with st.container():
    st.title('HCM City Weather Report Dashboard')

list_times_of_day = ['All'] + sorted(list(seven_days_df['times of day'].unique()))
# dynamic_filters = DynamicFilters(weather_df, 'name')
with st.sidebar:
    st.title('Filters')
    selected_tod = st.selectbox('Times of a day', list_times_of_day)
    # dynamic_filters.display_filters()

# filtered_df = dynamic_filters.filter_df()
filtered_df = seven_days_df

if selected_tod != 'All':
    filtered_df = filtered_df[filtered_df['times of day'] == selected_tod]

overall_weather = filtered_df['name_wc'].mode()[0]
avg_humidity = filtered_df['relative_humidity_2m'].mean()
max_visibility = filtered_df['visibility'].max()
avg_pressure = filtered_df['surface_pressure'].mean()
avg_cloud_cover = filtered_df['cloud_cover'].mean()

def get_wind_direction(deg):
    if deg >= 202.5 or deg < 247.6:
        return 'N'
    elif 247.5 <= deg < 292.6:
        return 'NE'
    elif 292.5 <= deg < 337.6:
        return 'E'
    elif 337.5 <= deg < 382.6:
        return 'SE'
    elif 22.5 <= deg < 427.6:
        return 'S'
    elif 67.5 <= deg < 112.6:
        return 'SW'
    elif 112.5 <= deg < 157.6:
        return 'W'
    else:
        return 'NW'

avg_wind_direction = filtered_df['wind_direction_80m'].apply(get_wind_direction).mode()[0]
avg_wind_speed = filtered_df['wind_speed_80m'].mean()
avg_wind_gust = filtered_df['wind_gusts_10m'].mean()

avg_wind_speed_by_day = filtered_df.groupby('date')['wind_speed_80m'].mean().reset_index()
avg_wind_gust_by_day = filtered_df.groupby('date')['wind_gusts_10m'].mean().reset_index()
wind_data_by_day = avg_wind_speed_by_day.merge(avg_wind_gust_by_day, on='date')

max_temp = filtered_df['temperature_2m'].max()
min_temp = filtered_df['temperature_2m'].min()
avg_temp = filtered_df['temperature_2m'].mean()

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric('Overall Weather', overall_weather)
    col2.metric('Avg Humidity', f'{avg_humidity:.2f}%')
    col3.metric('Max Visibility', f'{max_visibility:.2f} m')
    col4.metric('Cloud Cover', f'{avg_cloud_cover:.2f}%')
    col5.metric('Avg Pressure', f'{avg_pressure:.2f} hPa')

avg_temp_by_day = filtered_df.groupby('date')['temperature_2m'].mean().reset_index()
filtered_7days_df = filtered_df[['month_date', 'hour', 'temperature_2m']].sort_values(by=['month_date', 'hour'], ascending=False)

avg_uv = filtered_df['uv_index'].mean()
avg_sunshine = filtered_df['sunshine_duration'].mean()
avg_uv_by_date = filtered_df.groupby(['date'])['uv_index'].mean().reset_index()
avg_sunshine_by_date = filtered_df.groupby(['date'])['sunshine_duration'].mean().reset_index()

with st.container():
    st.subheader('Sunshine Duration and UV Index Reports')
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Avg UV Index', f'{avg_uv:.2f} mW/cm2')
        bar_chart_1 = px.bar(avg_uv_by_date, x='date', y='uv_index')
        bar_chart_1.update_layout(
            height=300,
        )
        st.plotly_chart(bar_chart_1, use_container_width=True)

    with col2:
        st.metric('Avg Sunshine Duration', f'{avg_sunshine:.2f} mins')
        bar_chart_2 = px.bar(avg_sunshine_by_date, x='date', y='sunshine_duration')
        bar_chart_2.update_layout(
            height=300,
        )
        st.plotly_chart(bar_chart_2, use_container_width=True)

with st.container():
    st.subheader('Temperature Reports')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric('Max Temp', f'{max_temp:.2f}°C')
    col3.metric('Min Temp', f'{min_temp:.2f}°C')
    col5.metric('Avg Temp', f'{avg_temp:.2f}°C')
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.write('AVG Temperature in the Last 7 Days')
        line_chart_1 = px.line(avg_temp_by_day, x='date', y='temperature_2m')
        st_line_1 = st.plotly_chart(line_chart_1, use_container_width=True)
    
    with col2:
        st.write('AVG Temperature by Hour')
        st.dataframe(filtered_7days_df.reset_index(drop=True), use_container_width=True)

with st.container():
    st.subheader('Wind Reports')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric('Avg Wind Direction', avg_wind_direction)
    col3.metric('Avg Wind Speed', f'{avg_wind_speed:.2f} m/s')
    col5.metric('Avg Wind Gust', f'{avg_wind_gust:.2f} m/s')
        
    st.write('AVG Wind Speed and Gust in the Last 7 Days')
    line_chart_2 = px.line(wind_data_by_day, x='date', y=['wind_speed_80m', 'wind_gusts_10m'],
                        labels={
        'value': 'Wind Speed (m/s)',
        'variable': 'Wind Metrics'})
    line_chart_2.update_layout(
        legend=dict(
            title='Wind Metrics',
            orientation='h', 
            yanchor='bottom',  
            y=1.1,  
            xanchor='center',  
            x=0.5 
            ),
        height=400
        )
    st_line_2 = st.plotly_chart(line_chart_2, use_container_width=True)
