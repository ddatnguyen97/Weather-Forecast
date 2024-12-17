import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from data import *
from metrics import *

def create_line_chart(df, x, y, title, color=None):
    fig = px.line(df, x=x, y=y, title=title, color=color)
    return fig

def create_bar_chart(df, x, y, title, color=None):
    fig = px.bar(df, x=x, y=y, title=title, color=color)
    return fig

def create_gauge_chart(value, title):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {"text": title},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    return fig

def create_area_chart(df, x, y, title, color=None):
    fig = px.area(df, x=x, y=y, title=title, color=color)
    return fig

def create_data_card(value, title):
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = value,
        title = {"text": title},
        domain = {'x': [0, 1], 'y': [0, 1]},

    ))
    return fig

temperature_chart = create_line_chart(avg_temp_by_day_hour, x='time', y='temperature_2m', title='Average Temperature by Hour', color='month_day')

sunshine_duration_chart = create_area_chart(sunshine_duration_by_day_hour, x='time', y='sunshine_duration', title='Average Sunshine Duration by Hour', color='month_day')
sunshine_duration_chart.update_layout(height=500)

wind_chart = create_line_chart(wind_data_by_day, x='time', y=['wind_speed_80m', 'wind_gusts_10m'], title='Wind Speed and Gust by Hour', color='month_day')

rainfall_chart = create_bar_chart(rainfall_data_by_day, x='time', y=['precipitation', 'rain', 'showers'], title='Rainfall by Hour', color='month_day')

avg_uv_index_chart = create_gauge_chart(metrics['avg_uv_index'], 'AVG UV Index (mW/cm2)')
avg_uv_index_chart.update_layout(height=240)
avg_uv_clear_sky_chart = create_gauge_chart(metrics['avg_uv_clear_sky'], 'AVG UV Index CS (mW/cm2)')
avg_uv_clear_sky_chart.update_layout(height=240)