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
        weather_df = clean_df(df, columns)
        return weather_df
    
    except Exception as e:
        logging.error(f"Error executing data code: {str(e)}")
        raise
