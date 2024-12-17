import pandas as pd
import logging

from data import *

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
    avg_humidity = calculate_avg(df, 'relative_humidity_2m')
    avg_precipitation = calculate_avg(df, 'precipitation')
    avg_rain = calculate_avg(df, 'rain')
    avg_showers = calculate_avg(df, 'showers')
    avg_dew_point = calculate_avg(df, 'dew_point_2m')
    avg_pressure_msl = calculate_avg(df, 'pressure_msl')
    avg_surface_pressure = calculate_avg(df, 'surface_pressure')
    avg_evapotranspiration = calculate_avg(df, 'evapotranspiration')
    avg_vapour_pressure_deficit = calculate_avg(df, 'vapour_pressure_deficit')
    comfort_level = calculate_mode(df, 'comfort_index')

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
        "avg_precipitation": f'{avg_precipitation:.2f} mm',
        "avg_rain": f'{avg_rain:.2f} mm',
        "avg_showers": f'{avg_showers:.2f} mm',
        "avg_dew_point": f'{avg_dew_point:.2f}°C',
        "avg_pressure_msl": f'{avg_pressure_msl:.2f} hPa',
        "avg_surface_pressure": f'{avg_surface_pressure:.2f} hPa',
        "avg_evapotranspiration": f'{avg_evapotranspiration:.2f} mm',
        "avg_vapour_pressure_deficit": f'{avg_vapour_pressure_deficit:.2f} hPa',
        "comfort_index": comfort_level,
    }

metrics = calculate_metrics(filter_7d_df)
