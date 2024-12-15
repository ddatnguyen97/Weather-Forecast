import pandas as pd
import logging
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
db_config = {
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'db_name': os.getenv('DB_NAME')
}
connection_string = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db_name']}"

def get_time(st, et):
    try:
        start_time = st
        end_time = et
        time_range = pd.date_range(start=start_time, end=end_time, freq='h')

        df = pd.DataFrame({
        'time': time_range
        })
        logging.info(f'data extracted: {df.shape[0]} rows')
        return df 

    except Exception as e:
        logging.error(f'error: {e}')
        raise

def transform_data(df):
    try:
        df['id'] = df['time'].dt.strftime('%H%M').astype(str)
        df['hour'] = df['time'].dt.hour
        df['id'] = df['id'].apply(lambda x: '0' + x if len(x) == 3 else x)
        df['id'] = df['id'].apply(lambda x: '00' + x if len(x) == 2 else x)
        df['id'] = df['id'].apply(lambda x: '000' + x if len(x) == 1 else x)
        df = df.drop_duplicates()
        logging.info(f'dropped duplicates: {df.shape[0]} rows')
        return df
    
    except Exception as e:
        logging.error(f'error: {e}')
        raise

def load_data_to_dw(df, table_name, connection_string):
    try:
        engine = create_engine(connection_string)

        with engine.connect() as connection:
            df.to_sql(table_name, con=connection, index=False, if_exists='append')
        logging.info(f'{df.shape[0]} date loaded to dw')

    except Exception as e:
        logging.error(f'error: {e}')
        raise

def execute_pipeline(st, et, table_name, connection_string):
    try:
        df = get_time(st, et)
        df = transform_data(df)
        load_data_to_dw(df, table_name, connection_string)
    
    except Exception as e:
        logging.error(f'error: {e}')
        raise

if __name__ == '__main__':
    table_name = 'dim_time'
    start_time = '00:00:00'
    end_time = '23:59:59'
    execute_pipeline(start_time, end_time, table_name, connection_string)