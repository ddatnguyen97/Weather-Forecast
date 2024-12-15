import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

API_URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"
LOCATION = {"latitude": 10.8231, "longitude": 106.6297}
DATE_RANGE = {"start_date": "2022-01-01", "end_date": "2024-12-10"}
HOURLY_VARIABLES = [
        "temperature_2m",
        "relative_humidity_2m",
        "dew_point_2m",
        "apparent_temperature", 
        "precipitation_probability", 
        "rain", 
        "showers",
        "weather_code", 
        "pressure_msl", 
        "surface_pressure", 
        "cloud_cover", 
        "visibility", 
        "evapotranspiration", 
        "vapour_pressure_deficit", 
        "wind_speed_80m", 
        "wind_direction_80m", 
        "wind_gusts_10m", 
        "temperature_80m", 
        "uv_index", 
        "uv_index_clear_sky", 
        "is_day", 
        "sunshine_duration"
    ]

db_config = {
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'db_name': os.getenv('DB_NAME')
}
connection_string = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db_name']}"

def fetch_weather_data():
    try:
        params = {
            **LOCATION,
            **DATE_RANGE,
            "hourly": HOURLY_VARIABLES,
            "cell_selection": "nearest"
        }
        response = openmeteo.weather_api(API_URL, params=params)[0]
        logging.info(f"Data fetched for coordinates: {response.Latitude()}°N, {response.Longitude()}°E")
        return response
    except Exception as e:
        logging.error(f"Error fetching weather data: {str(e)}")
        raise

def extract_hourly_data(response):
    try:
        hourly = response.Hourly()
        hourly_data = {
            variable: hourly.Variables(idx).ValuesAsNumpy() for idx, variable in enumerate(HOURLY_VARIABLES)
        }
        hourly_data["date"] = pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
        df = pd.DataFrame(hourly_data)
        logging.info(f"Extracted {df.shape[0]} hourly rows.")
        return df
    except Exception as e:
        logging.error(f"Error extracting hourly data: {str(e)}")
        raise

def transform_data(df):
    try:
        df['weather_code'] = df['weather_code'].fillna(df['weather_code'].mode()[0])
        df['is_day'] = df['is_day'].fillna(df['is_day'].mode()[0])

        df['date_id'] = df['date'].dt.strftime('%Y%m%d')
        df['time_id'] = df['date'].dt.strftime('%H%M')
        df['weather_code'] = df['weather_code'].astype(int).apply(lambda x: f"{x:02d}")
        df['is_day'] = df['is_day'].astype(int).apply(lambda x: f"{x:02d}")
        df.drop(columns=['date'], inplace=True)
        df['id'] = df['date_id'] + df['time_id']
        logging.info(f"Transformed data with {df.shape[1]} columns.")
        return df
    except Exception as e:
        logging.error(f"Error transforming data: {str(e)}")
        raise

def load_data_to_dw(df, table_name):
    try:
        engine = create_engine(connection_string)
        df.to_sql(table_name, con=engine, index=False, if_exists='append')
        logging.info(f"Loaded {df.shape[0]} rows into table '{table_name}'.")
    except Exception as e:
        logging.error(f"Error loading data to database: {str(e)}")
        raise

def execute_pipeline(table_name):
    try:
        logging.info("Pipeline execution started.")
        response = fetch_weather_data()
        df = extract_hourly_data(response)
        df = transform_data(df)
        load_data_to_dw(df, table_name)
        logging.info("Pipeline execution completed successfully.")
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == '__main__':
    table_name = 'hcm_weather'
    df = execute_pipeline(table_name)
