import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from app import app
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq as pd1
from google.cloud import bigquery
import os
from datetime import datetime

layout = html.Div([

    dbc.Row([
        dbc.Col([
            html.P('Type country name', style={'color': '#666666'}),
            dcc.Input(id='country_name',
                      style={'margin-top': '-10px'})
        ]),
        dbc.Col([
            html.P('Select product', style={'color': '#666666'}),
            dcc.Dropdown(
                id='select_product',
                options=['Bread', 'Eggs', 'Yogurt', 'Coconut cream'],
                searchable=True,
                clearable=True,
                style={'margin-top': '-5px', 'width': '190px'})
        ]),
        dbc.Col([
            html.P('Type price', style={'color': '#666666'}),
            dcc.Input(id='sales_value',
                      style={'margin-top': '-10px'})
        ]),
        dbc.Col([
            html.P('Type quantity', style={'color': '#666666'}),
            dcc.Input(id='quantity_value',
                      style={'margin-top': '-10px'})
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Button('Add Data',
                        id='add_data',
                        n_clicks=0)
        ])
    ]),

    html.Div(id='insert_data', children=[])
])


@app.callback(Output('insert_data', 'children'),
              [Input('add_data', 'n_clicks')],
              [State('select_product', 'value')],
              [State('country_name', 'value')],
              [State('sales_value', 'value')],
              [State('quantity_value', 'value')],
              prevent_initial_call=True)
def update_value(n_clicks, select_product, country_name, sales_value, quantity_value):
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    selectProduct = select_product
    countryName = country_name
    salesValue = sales_value
    quantityValue = quantity_value

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'crud.json'

    client = bigquery.Client()
    table_id = 'data-streaming-368616.crudDatabase.crudTable'

    rows_to_insert = [
        {u'Country': countryName,
         u'Sales': salesValue,
         u'Product': selectProduct,
         u'DateTime': dt_string,
         u'Quantity': quantityValue}
    ]

    if n_clicks > 0:
        return [
            client.insert_rows_json(table_id, rows_to_insert)
        ]
