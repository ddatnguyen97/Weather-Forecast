from sqlalchemy import create_engine, text
import pandas as pd
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
            return result
    
    except Exception as e:
        logging.error(f"Error fetching weather data: {str(e)}")
        raise

def convert_to_df(df):
    try:
        columns = df.keys()
        values = df.fetchall()
        return pd.DataFrame(values, columns=columns)
    
    except Exception as e:
        logging.error(f"Error converting query to DataFrame: {str(e)}")
        raise

def clean_df(df, cols):
    try:
        df.drop(columns=cols, inplace=True)
        return df
    
    except Exception as e:
        logging.error(f"Error cleaning DataFrame: {str(e)}")
        raise

def execute_data_code(query, columns):
    try:
        result = fetch_data(query)
        df = convert_to_df(result)
        cleaned_df = clean_df(df, columns)
        return cleaned_df
    
    except Exception as e:
        logging.error(f"Error executing data code: {str(e)}")
        raise

query = text("""
    select 
        hw.*,
        dd.date,
        dd.quarter,
        dd.year,
        dd.month,
        dd.day,
        dt.time,
        tod.name as time_of_day,
        wc.name as weather_code_name   
    from
        hourly_weather_data hw 
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
    'precipitation_probability', 'precipitation', 'rain', 'showers', 'pressure_msl', 'surface_pressure',
    'cloud_cover', 'visibility', 'evapotranspiration', 'vapour_pressure_deficit', 
    'wind_speed_10m', 'wind_direction_10m', 'wind_gusts_10m', 
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

def get_comfort_index(dew_point):
    if dew_point < 4.4:
        return "Very Dry"
    elif 4.4 <= dew_point < 10:
        return "Dry"
    elif 10 <= dew_point < 15.5:
        return "Comfortable"
    elif 15.5 <= dew_point < 18.3:
        return "Slightly Humid"
    elif 18.3 <= dew_point < 21.1:
        return "Humid"
    elif 21.1 <= dew_point < 23.9:
        return "Very Humid"
    else:
        return "Extremely Humid" 

weather_df['date'] = pd.to_datetime(weather_df['date'])
weather_df['month_day'] = weather_df['date'].dt.strftime('%m-%d')
weather_df['year_month'] = weather_df['date'].dt.strftime('%Y-%m')
weather_df['wind_direction'] = weather_df['wind_direction_10m'].apply(get_wind_direction)
weather_df['comfort_index'] = weather_df['dew_point_2m'].apply(get_comfort_index)

def filter_7d_data(df, day=None, offset=7):
    if day is None:
        current_date = pd.Timestamp.now().normalize() - pd.DateOffset(days=1)
    else:
        current_date = pd.Timestamp(day).normalize()

    cutoff_date = current_date - pd.DateOffset(days=offset)
    return df[(df['date'] > cutoff_date) & (df['date'] <= current_date)]


def filter_5y_data(df, year='year', offset=5):
    current_year = pd.Timestamp.now().year
    cutoff_year = max(df[year].min(), current_year - offset)
    return df[df[year] >= cutoff_year]