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

def create_hist_chart(df, x, title, color=None):
    fig = px.histogram(df, x=x, title=title, color=color)
    return fig

def create_choropleth_map(df, lat, lon, color, title=None):
    fig = px.choropleth(df,
        lat=lat,
        lon=lon,
        color=color,
        title=title)
    return fig

def create_combine_chart(datasets, labels, x_column, y_column, title, x_title, y_title, chart_types, colors=None):
    fig = go.Figure()
    for i, dataset in enumerate(datasets):
        if chart_types[i] == 'line':
            fig.add_trace(go.Scatter(
            x=dataset[x_column],
            y=dataset[y_column[i]],
            name=labels[i], 
            mode=None, 
            line=dict(color=colors[i])
            ))
        elif chart_types[i] == 'bar':
            fig.add_trace(go.Bar(
            x=dataset[x_column],
            y=dataset[y_column[i]],
            name=labels[i],
            marker_color=colors[i]
            ))
    fig.update_layout(title=title, xaxis_title=x_title, yaxis_title=y_title)
    return fig

def create_choropleth_map(df, geojson, locations, color, title=None):
    fig = px.choropleth(df,
        geojson=geojson,
        locations=locations,
        color=color,
        title=title)
    return fig

def create_mapbox_map(df, lat, lon, color, title=None):
    fig = px.scatter_mapbox(
        df,
        lat=lat,
        lon=lon,
        color=color,
        title=title,
        mapbox_style="carto-positron",
        zoom=10
    )
    return fig