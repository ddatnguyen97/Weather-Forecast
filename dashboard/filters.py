import pandas as pd

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

def filter_column(df, column, selected_value, default="All"):
    if selected_value != default:
        return df[df[column] == selected_value]
    return df