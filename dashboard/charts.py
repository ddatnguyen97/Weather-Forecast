import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from data import *
from metrics import *

def create_line_chart(df, x, y, title, color=None):
    fig = px.line(df, x=x, y=y, title=title, color=color)
    return fig

def create_bar_chart(df, x, y, title, color=None):
    fig = px.bar(df, x=x, y=y, title=title, color=color)
    return fig

def create_gauge_chart(value, title):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {"text": title},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    return fig

def create_area_chart(df, x, y, title, color=None):
    fig = px.area(df, x=x, y=y, title=title, color=color)
    return fig

def create_data_card(value, title):
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = value,
        title = {"text": title},
        domain = {'x': [0, 1], 'y': [0, 1]},

    ))
    return fig
