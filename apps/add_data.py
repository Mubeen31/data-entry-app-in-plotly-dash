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

    html.Div(id='insert_data', children=[]),

    html.Div([
        html.Div([
            html.P(dcc.Markdown('''Insert data using the below button in the **Google Big Query** Database.'''),
                   style={'margin-bottom': '-10px', 'color': 'black'}),
            dbc.Button("Add Data",
                       id="open-centered",
                       n_clicks=0,
                       class_name='text_size'),
        ], className='button_text'),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Add data using the below cells."),
                            close_button=True),
            dbc.ModalBody([
                html.Div([
                    html.Div([
                        html.P('Type country name', style={'color': 'white'}),
                        dcc.Input(id='country_name',
                                  placeholder='Type country name',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Select product', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='select_product',
                            placeholder='Select product',
                            options=['Bread', 'Eggs', 'Yogurt', 'Coconut cream'],
                            searchable=True,
                            clearable=True,
                            style={'margin-top': '-5px', 'width': '190px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Type price', style={'color': 'white'}),
                        dcc.Input(id='sales_value',
                                  placeholder='Type price value',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Type quantity', style={'color': 'white'}),
                        dcc.Input(id='quantity_value',
                                  placeholder='Type number of quantities',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                ], className='input_row'),

                html.Div([
                    dbc.Button('Submit Data',
                               id='add_data',
                               n_clicks=0,
                               class_name='text_size')
                ], className='button_row'),
            ]),
            dbc.ModalFooter(dbc.Button("Close",
                                       id="close-centered",
                                       className="ms-auto",
                                       n_clicks=0))
        ], id="modal-centered",
            centered=True,
            is_open=False,
            size="xl"),
    ], className='modal_row'),

    html.Div([
        dbc.Modal([
            dbc.ModalBody("Data has been added. To view data, visit the 'Analyze Data' link.",
                          style={'color': 'white'}),
            dbc.ModalFooter(
                dbc.Button("Close",
                           id="data_added_close",
                           className="ms-auto",
                           n_clicks=0
                           )
            ),
        ], id="data_added_modal",
            is_open=False
        )
    ])
])


@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks")],
    [Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("data_added_modal", "is_open"),
    [Input("add_data", "n_clicks")],
    [Input("data_added_close", "n_clicks")],
    [State("data_added_modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


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
