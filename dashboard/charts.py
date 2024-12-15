import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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

def create_pivot_table(df, values, index, columns):
    table = pd.pivot_table(df, values=values, index=index, columns=columns)
    return table

def create_data_card(value, title):
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = value,
        title = {"text": title},
        domain = {'x': [0, 1], 'y': [0, 1]},

    ))
    return fig

# filter_7d_df = filter_7d_data(weather_df)

# temperature_chart = create_line_chart(
#         avg_temp_by_day_hour,
#         'time', 
#         'temperature_2m', 
#         'Average Temperature by Day',
#         'month_day')
# temperature_chart.update_layout(
#         height=500,
#     )

# avg_uv_index_chart = create_gauge_chart(avg_uv_index, 'AVG UV Index (mW/cm2)')
# avg_uv_index_chart.update_layout(
#         height=250,
#     )

# avg_uv_clear_sky_chart = create_gauge_chart(avg_uv_clear_sky, 'AVG UV Index CS (mW/cm2)')
# avg_uv_clear_sky_chart.update_layout(
#         height=250,
#     )

# sunshine_duration_chart = create_area_chart(
#         sunshine_duration_by_day_hour,
#         'time',
#         'sunshine_duration',
#         'Average Sunshine Duration by Hour',
#         'month_day')
# sunshine_duration_chart.update_layout(
#         height=500,
#     )

# wind_chart = create_line_chart(
#         wind_data_by_day,
#         'time',
#         ['wind_speed_80m', 'wind_gusts_10m'],
#         'Average Wind Speed and Gust by Day',
#         'month_day')

def generate_dashboard_charts(avg_temp_by_day_hour, sunshine_duration_by_day_hour, wind_data_by_day, metrics):
    # Temperature Chart
    temperature_chart = create_line_chart(
        avg_temp_by_day_hour,
        x='time', 
        y='temperature_2m', 
        title='Average Temperature by Day',
        color='month_day'
    )
    temperature_chart.update_layout(height=500)

    # UV Index Charts
    avg_uv_index_chart = create_gauge_chart(metrics['avg_uv_index'], 'AVG UV Index (mW/cm2)')
    avg_uv_index_chart.update_layout(height=250)

    avg_uv_clear_sky_chart = create_gauge_chart(metrics['avg_uv_clear_sky'], 'AVG UV Index CS (mW/cm2)')
    avg_uv_clear_sky_chart.update_layout(height=250)

    # Sunshine Duration Chart
    sunshine_duration_chart = create_area_chart(
        sunshine_duration_by_day_hour,
        x='time',
        y='sunshine_duration',
        title='Average Sunshine Duration by Hour',
        color='month_day'
    )
    sunshine_duration_chart.update_layout(height=500)

    # Wind Chart
    wind_chart = create_line_chart(
        wind_data_by_day,
        x='time',
        y=['wind_speed_80m', 'wind_gusts_10m'],
        title='Average Wind Speed and Gust by Day',
        color='month_day'
    )

    return {
        "temperature_chart": temperature_chart,
        "avg_uv_index_chart": avg_uv_index_chart,
        "avg_uv_clear_sky_chart": avg_uv_clear_sky_chart,
        "sunshine_duration_chart": sunshine_duration_chart,
        "wind_chart": wind_chart
    }