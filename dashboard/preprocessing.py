import pandas as pd

from data import *

query = text("""
    select 
        hW.*,
        dd.date,
        dd.quarter,
        dd.year,
        dd.month,
        dd.day,
        dt.time,
        tod.name as time_of_day,
        wc.name as weather_code_name   
    from
        hcm_weather hw 
    join
        dim_date dd on hw.date_id = dd.id
    join
        dim_time dt on hw.time_id = dt.id
    join 
        times_of_day tod on hw.is_day = tod.id
    join
        weather_code wc on hw.weather_code = wc.id
        """)

columns_to_drop = ['id',
                    'date_id',
                    'time_id',
                    'is_day',
                    'weather_code',
                    ]

weather_df = execute_data_code(query, columns_to_drop)

numeric_columns = [
    'temperature_2m', 'relative_humidity_2m', 'dew_point_2m', 'apparent_temperature',
    'precipitation_probability', 'rain', 'showers', 'pressure_msl', 'surface_pressure',
    'cloud_cover', 'visibility', 'evapotranspiration', 'vapour_pressure_deficit', 
    'wind_speed_80m', 'wind_direction_80m', 'wind_gusts_10m', 'temperature_80m', 
    'uv_index', 'uv_index_clear_sky', 'sunshine_duration'
]
for col in numeric_columns:
    weather_df[col] = pd.to_numeric(weather_df[col], errors='coerce')

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

weather_df['date'] = pd.to_datetime(weather_df['date'])
weather_df['month_day'] = weather_df['date'].dt.strftime('%m-%d')
weather_df['wind_direction'] = weather_df['wind_direction_80m'].apply(get_wind_direction)
print(weather_df.info())

def filter_7d_data(df, days=6):
    max_date = df['date'].max()
    cutoff_date = max_date - pd.DateOffset(days=days)
    return df[df['date'] >= cutoff_date]

weather_df = weather_df