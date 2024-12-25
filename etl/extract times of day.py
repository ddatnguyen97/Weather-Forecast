import pandas as pd
import logging
import openpyxl
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

def extract_data(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name, engine='openpyxl')
        logging.info(f'{file_path} has been read successfully.')
        return df
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')
        return None


def transform_data(df):
    try:
        df['id'] = df['id'].astype(str)
        df['id'] = df['id'].apply(lambda x: '0' + x if len(x) == 1 else x)
        return df
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')
        raise

def load_data_to_dw(df, table_name, connection_string):
    try:
        engine = create_engine(connection_string)
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        logging.info(f'Data has been loaded to {table_name} successfully.')
    
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')
        raise

def execute_pipeline(file_path, sheet_name, table_name, connection_string):
    try:
        df = extract_data(file_path, sheet_name)
        transformed_df = transform_data(df)
        load_data_to_dw(transformed_df, table_name, connection_string)

    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')
        raise

if __name__ == '__main__':
    file_path = 'weather mapping.xlsx'
    sheet_name = 'times_of_day'
    table_name = 'times_of_day'
    execute_pipeline(file_path, sheet_name, table_name, connection_string)