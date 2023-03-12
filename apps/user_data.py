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

    html.Div(id='insert_user_data', children=[]),

    html.Div([
        html.Div([
            dbc.Button("Add Data",
                       id="open-centered-user",
                       n_clicks=0,
                       class_name='text_size'),
        ], className='button_text'),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Add data using the below cells."),
                            close_button=True),
            dbc.ModalBody([
                html.Div([
                    html.Div([
                        html.P('First name', style={'color': 'white'}),
                        dcc.Input(id='first_name',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Last name', style={'color': 'white'}),
                        dcc.Input(id='last_name',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Email', style={'color': 'white'}),
                        dcc.Input(id='email_address',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Address', style={'color': 'white'}),
                        dcc.Input(id='living_address',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Country name', style={'color': 'white'}),
                        dcc.Input(id='name_country',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Mobile no.', style={'color': 'white'}),
                        dcc.Input(id='mobile_number',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                ], className='input_row'),

                html.Div([
                    dbc.Button('Add Data',
                               id='insert_user_data_button',
                               n_clicks=0,
                               class_name='text_size')
                ], className='button_row'),
            ]),
            dbc.ModalFooter(dbc.Button("Close",
                                       id="close-centered-user",
                                       className="ms-auto",
                                       n_clicks=0))
        ], id="modal-centered-user",
            centered=True,
            is_open=False,
            size="xl"),
    ], className='modal_row'),

    html.Div([
        dbc.Modal([
            dbc.ModalBody("Data has been added. View the inserted data in the below table.",
                          style={'color': 'white'}),
            dbc.ModalFooter(
                dbc.Button("Close",
                           id="user_data_added_close",
                           className="ms-auto",
                           n_clicks=0
                           )
            ),
        ], id="user_data_added_modal",
            is_open=False
        )
    ])
])


@app.callback(
    Output("modal-centered-user", "is_open"),
    [Input("open-centered-user", "n_clicks")],
    [Input("close-centered-user", "n_clicks")],
    [State("modal-centered-user", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("user_data_added_modal", "is_open"),
    [Input("insert_user_data_button", "n_clicks")],
    [Input("user_data_added_close", "n_clicks")],
    [State("user_data_added_modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(Output('insert_user_data', 'children'),
              [Input('insert_user_data_button', 'n_clicks')],
              [State('first_name', 'value')],
              [State('last_name', 'value')],
              [State('email_address', 'value')],
              [State('living_address', 'value')],
              [State('name_country', 'value')],
              [State('mobile_number', 'value')],
              prevent_initial_call=True)
def update_value(n_clicks, first_name, last_name, email_address, living_address, name_country, mobile_number):
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    firtsName = first_name
    lastName = last_name
    email = email_address
    livingAdddress = living_address
    countryName = name_country
    mobileNumber = mobile_number

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'crud.json'

    client = bigquery.Client()
    table_id = 'data-streaming-368616.userDatabase.userDataRecord'

    rows_to_insert = [
        {u'FirstName': firtsName,
         u'LastName': lastName,
         u'Email': email,
         u'Address': livingAdddress,
         u'CountryName': countryName,
         u'MobileNo': mobileNumber,
         u'DateTime': dt_string}
    ]

    if n_clicks > 0:
        return [
            client.insert_rows_json(table_id, rows_to_insert)
        ]
