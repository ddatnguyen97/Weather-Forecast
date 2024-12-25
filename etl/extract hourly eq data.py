import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

start_date = (pd.Timestamp.now().normalize() - pd.DateOffset(days=1)).strftime('%Y-%m-%d')
end_date = (pd.Timestamp.now().normalize() - pd.DateOffset(days=1)).strftime('%Y-%m-%d')

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
LOCATION = {"latitude": 10.8231, "longitude": 106.6297}
# DATE_RANGE = {"start_date": start_date, "end_date": end_date}
DATE_RANGE = {"start_date": '2022-01-01', "end_date": '2024-12-24'}

HOURLY_VARIABLES = [
    "pm10", 
    "pm2_5", 
    "carbon_monoxide", 
    "carbon_dioxide", 
    "nitrogen_dioxide", 
    "sulphur_dioxide", 
    "ozone", 
    "aerosol_optical_depth", 
    "dust", 
    "methane",
    ]

db_config = {
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'db_name': os.getenv('DB_NAME')
}
connection_string = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db_name']}"

def fetch_air_quality_data():
    try:
        params = {
            **LOCATION,
            **DATE_RANGE,
            "hourly": HOURLY_VARIABLES,
        }
        response = openmeteo.weather_api(API_URL, params=params)[0]
        logging.info(f"Data fetched for coordinates: {response.Latitude()}°N, {response.Longitude()}°E")
        return response
    except Exception as e:
        logging.error(f"Error fetching air quality data: {e}")
        raise

def extract_data(response):
    try:
        hourly = response.Hourly()
        hourly_data = {
            variable: hourly.Variables(idx).ValuesAsNumpy() for idx, variable in enumerate(HOURLY_VARIABLES)
        }
        hourly_data['date'] = pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
        df = pd.DataFrame(hourly_data)
        logging.info(f"Extracted {df.shape[0]} hourly rows.")
        return df
    except Exception as e:
        logging.error(f"Error extracting data: {str(e)}")
        raise

def transform_data(df):
    try:
        df['date_id'] = df['date'].dt.strftime('%Y%m%d')
        df['time_id'] = df['date'].dt.strftime('%H%M')
        df.drop(columns=['date'], inplace=True)
        df['id'] = df['date_id'] + df['time_id']
        logging.info(f"Transformed data with {df.shape[1]} columns.")
        return df
    except Exception as e:
        logging.error(f"Error transforming data: {str(e)}")
        raise

def insert_on_conflict_nothing(table, conn, keys, data_iter):
    try:
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = insert(table.table).values(data).on_conflict_do_nothing(index_elements=["id"])
        result = conn.execute(stmt)
        return result.rowcount
    
    except Exception as e:
        logging.error(f'error during insert: {e}')
        raise

def load_data_to_dw(df, table_name, method=insert_on_conflict_nothing):
    try:
        engine = create_engine(connection_string)
        df.to_sql(table_name, con=engine, index=False, if_exists='append', method=method)
        logging.info(f"Loaded {df.shape[0]} rows into table '{table_name}'.")
    except Exception as e:
        logging.error(f"Error loading data to database: {str(e)}")
        raise

def execute_pipeline(table_name):
    try:
        logging.info("Pipeline execution started.")
        response = fetch_air_quality_data()
        df = extract_data(response)
        df = transform_data(df)
        load_data_to_dw(df, table_name)
        logging.info("Pipeline execution completed successfully.")
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == '__main__':
    table_name = 'hourly_aq_data'
    df = execute_pipeline(table_name)