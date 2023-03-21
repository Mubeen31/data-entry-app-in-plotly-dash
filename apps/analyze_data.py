from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from app import app
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq as pd1

layout = html.Div([

    dcc.Interval(id='update_data',
                 interval=1 * 5000,
                 n_intervals=0),

    html.Div([
        html.Div(id='total_sales',
                 className='background_card'),
        html.Div(id='total_product',
                 className='background_card'),
        html.Div(id='total_quantity',
                 className='background_card'),
        html.Div(id='total_ordered',
                 className='background_card')
    ], className='card_row')
])


@app.callback(Output('total_sales', 'children'),
              [Input('update_data', 'n_interval')])
def display_table(update_data):
    credentials = service_account.Credentials.from_service_account_file('crud.json')
    project_id = 'data-streaming-368616'
    df_sql = f"""SELECT
                 Sales
                 FROM
                 `data-streaming-368616.crudDatabase.crudTable`
                 """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    total_sales = df3['Sales'].sum()

    return [
        html.Div('Total Sales',
                 style={'color': '#a6a6a6',
                        'margin-left': '10px',
                        'margin-top': '5px'}),
        html.Div([
            html.Div('{0:,.0f}'.format(total_sales),
                     className='numeric_value'),
            html.Div('$', className='symbol')
        ], className='numeric_value_center')
    ]


@app.callback(Output('total_product', 'children'),
              [Input('update_data', 'n_interval')])
def display_table(update_data):
    credentials = service_account.Credentials.from_service_account_file('crud.json')
    project_id = 'data-streaming-368616'
    df_sql = f"""SELECT
                 Product
                 FROM
                 `data-streaming-368616.crudDatabase.crudTable`
                 """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df3 = df3.dropna(how='any', axis=0)
    total_product_sold = df3['Product'].nunique()

    return [
        html.Div('Total Product',
                 style={'color': '#a6a6a6',
                        'margin-left': '10px',
                        'margin-top': '5px'}),
        html.Div([
            html.Div('{0:,.0f}'.format(total_product_sold),
                     className='numeric_value'),
        ], className='numeric_value_center')
    ]


@app.callback(Output('total_quantity', 'children'),
              [Input('update_data', 'n_interval')])
def display_table(update_data):
    credentials = service_account.Credentials.from_service_account_file('crud.json')
    project_id = 'data-streaming-368616'
    df_sql = f"""SELECT
                 Quantity
                 FROM
                 `data-streaming-368616.crudDatabase.crudTable`
                 """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df3 = df3.dropna(how='any', axis=0)
    total_quantity = df3['Quantity'].sum()

    return [
        html.Div('Total Quantity',
                 style={'color': '#a6a6a6',
                        'margin-left': '10px',
                        'margin-top': '5px'}),
        html.Div([
            html.Div('{0:,.0f}'.format(total_quantity),
                     className='numeric_value'),
        ], className='numeric_value_center')
    ]


@app.callback(Output('total_ordered', 'children'),
              [Input('update_data', 'n_interval')])
def display_table(update_data):
    credentials = service_account.Credentials.from_service_account_file('crud.json')
    project_id = 'data-streaming-368616'
    df_sql = f"""SELECT
                 DateTime
                 FROM
                 `data-streaming-368616.crudDatabase.crudTable`
                 """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df3 = df3.dropna(how='any', axis=0)
    total_ordered = df3['DateTime'].nunique()

    return [
        html.Div('Total Ordered',
                 style={'color': '#a6a6a6',
                        'margin-left': '10px',
                        'margin-top': '5px'}),
        html.Div([
            html.Div('{0:,.0f}'.format(total_ordered),
                     className='numeric_value'),
        ], className='numeric_value_center')
    ]
