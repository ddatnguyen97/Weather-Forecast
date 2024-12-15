import pandas as pd
import logging

from preprocessing import *

def calculate_avg(df, column):
    avg = df[column].mean()
    return avg

def calculate_max(df, column):
    max_value = df[column].max()
    return max_value

def calculate_min(df, column):
    min_value = df[column].min()
    return min_value

def calculate_mode(df, column):
    mode = df[column].mode()
    return mode[0]

def calculate_metrics(df):
    overall_weather = calculate_mode(df, 'weather_code_name')
    avg_humidity = calculate_avg(df, 'relative_humidity_2m')
    avg_cloud_cover = calculate_avg(df, 'cloud_cover')
    max_visibility = calculate_max(df, 'visibility')
    max_temp = calculate_max(df, 'temperature_2m')
    min_temp = calculate_min(df, 'temperature_2m')
    avg_temp = calculate_avg(df, 'temperature_2m')
    wind_speed = calculate_avg(df, 'wind_speed_80m')
    wind_gust = calculate_avg(df, 'wind_gusts_10m')
    overall_wind_direction = calculate_mode(df, 'wind_direction')
    avg_uv_index = calculate_avg(df, 'uv_index')
    avg_uv_clear_sky = calculate_avg(df, 'uv_index_clear_sky')
    sunshine_duration = calculate_avg(df, 'sunshine_duration')

    # Return metrics in a structured format
    return {
        "overall_weather": overall_weather,
        "avg_humidity_f": f'{avg_humidity:.2f}%',
        "avg_cloud_cover_f": f'{avg_cloud_cover:.2f}%',
        "max_visibility_f": f'{max_visibility} m',
        "max_temp_f": f'{max_temp:.2f}°C',
        "min_temp_f": f'{min_temp:.2f}°C',
        "avg_temp_f": f'{avg_temp:.2f}°C',
        "wind_speed_f": f'{wind_speed:.2f} m/s',
        "wind_gust_f": f'{wind_gust:.2f} m/s',
        "overall_wind_direction": overall_wind_direction,
        "avg_uv_index": avg_uv_index,
        "avg_uv_clear_sky": avg_uv_clear_sky,
        "sunshine_duration": sunshine_duration,
    }

# filter_7d_df = filter_7d_data(weather_df)

# overall_weather = calculate_mode(filter_7d_df, 'weather_code_name')

# avg_humidity = calculate_avg(filter_7d_df, 'relative_humidity_2m')
# avg_humidity_f = f'{avg_humidity:.2f}%'

# avg_cloud_cover = calculate_avg(filter_7d_df, 'cloud_cover')
# avg_cloud_cover_f = f'{avg_cloud_cover:.2f}%'

# max_visibility = calculate_max(filter_7d_df, 'visibility')
# max_visibility_f = f'{max_visibility} m'

# max_temp = calculate_max(filter_7d_df, 'temperature_2m')
# max_temp_f = f'{max_temp:.2f}°C'
# min_temp = calculate_min(filter_7d_df, 'temperature_2m')
# min_temp_f = f'{min_temp:.2f}°C'
# avg_temp = calculate_avg(filter_7d_df, 'temperature_2m')
# avg_temp_f = f'{avg_temp:.2f}°C'
# avg_temp_by_day_hour = filter_7d_df.groupby(['month_day', 'time'])['temperature_2m'].mean().reset_index()

# avg_uv_index = calculate_avg(filter_7d_df, 'uv_index')
# avg_uv_clear_sky = calculate_avg(filter_7d_df, 'uv_index_clear_sky')
# sunshine_duration = calculate_avg(filter_7d_df, 'sunshine_duration')
# sunshine_duration_by_day_hour = filter_7d_df.groupby(['month_day', 'time'])['sunshine_duration'].mean().reset_index()

# wind_speed = calculate_avg(filter_7d_df, 'wind_speed_80m')
# wind_speed_f = f'{wind_speed:.2f} m/s'
# wind_direction = calculate_avg(filter_7d_df, 'wind_direction_80m')
# wind_gust = calculate_avg(filter_7d_df, 'wind_gusts_10m')
# wind_gust_f = f'{wind_gust:.2f} m/s'
# overall_wind_direction = calculate_mode(filter_7d_df, 'wind_direction')
# wind_data_by_day = filter_7d_df.groupby(['month_day', 'time'])[['wind_speed_80m', 'wind_gusts_10m']].mean().reset_index()