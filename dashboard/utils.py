import pandas as pd
import json
import os

def get_unique_sorted_list(df, column, ascending=False):
    return sorted(df[column].unique(), reverse=ascending)

def get_geojson(file_path):
    with open(f'{file_path}') as f:
        geojson = json.load(f)
    return geojson

hcm_geojson = get_geojson(os.getenv('HCM_GEOJSON_PATH'))