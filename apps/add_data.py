from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq as pd1
from google.cloud import bigquery
import os
from datetime import datetime
from dash import dash_table

credentials = service_account.Credentials.from_service_account_file('crud.json')
project_id = 'data-streaming-368616'
df_sql = f"""SELECT
             DateTime,
             Country,
             Product,
             Sales,
             Quantity
             FROM
             `data-streaming-368616.crudDatabase.crudTable`
             ORDER BY
             DateTime DESC LIMIT 1
             """
df4 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)

layout = html.Div([

    html.Div(id='insert_data', children=[]),

    html.Div([
        html.Div([
            html.P(dcc.Markdown('''Insert sales data using the below button in the **Google Big Query** Database.'''),
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
                        html.P('Select country', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='country_name',
                            placeholder='Select country',
                            options=['Australia', 'Brazil', 'India', 'Pakistan', 'Canada', 'France', 'Germany', 'USA',
                                     'UK', 'China', 'Russia', 'Bangladesh', 'Spain', 'Nigeria'],
                            searchable=True,
                            clearable=True,
                            style={'margin-top': '-5px', 'width': '190px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Type product name', style={'color': 'white'}),
                        dcc.Input(id='product_name',
                                  placeholder='Type product name',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Type price', style={'color': 'white'}),
                        dcc.Input(id='sales_value',
                                  placeholder='Type price value',
                                  minLength=0,
                                  maxLength=3,
                                  value='',
                                  style={'margin-top': '-10px', 'color': 'black'})
                    ], className='input_column'),
                    html.Div([
                        html.P('Type quantity', style={'color': 'white'}),
                        dcc.Input(id='quantity_value',
                                  placeholder='Type quantity value',
                                  minLength=0,
                                  maxLength=2,
                                  value='',
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
            dbc.ModalBody("Data has been added. View data in the below table and visit the 'Analyze Data' link.",
                          style={'color': 'black'}),
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
    ]),

    html.Div([
        dbc.Spinner(html.Div([dash_table.DataTable(id='my_datatable',
                                                   columns=[{"name": i, "id": i} for i in df4.columns],
                                                   page_size=13,
                                                   sort_action="native",
                                                   sort_mode="multi",
                                                   virtualization=True,
                                                   style_cell={'textAlign': 'left',
                                                               'min-width': '100px',
                                                               'backgroundColor': 'rgba(255, 255, 255, 0)',
                                                               'minWidth': 180,
                                                               'maxWidth': 180,
                                                               'width': 180},
                                                   style_header={
                                                       'backgroundColor': 'black',
                                                       'fontWeight': 'bold',
                                                       'font': 'Lato, sans-serif',
                                                       'color': 'orange',
                                                       'border': '1px solid white',
                                                   },
                                                   style_data={'textOverflow': 'hidden',
                                                               'color': 'black',
                                                               'fontWeight': 'bold',
                                                               'font': 'Lato, sans-serif'},
                                                   fixed_rows={'headers': True},
                                                   )
                              ], className='bg_table'), color='success')
    ], className='bg_container')
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
              Output('product_name', 'value'),
              Output('country_name', 'value'),
              Output('sales_value', 'value'),
              Output('quantity_value', 'value'),
              [Input('add_data', 'n_clicks')],
              [State('product_name', 'value')],
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
        ], '', '', '', ''


@app.callback(Output('my_datatable', 'data'),
              [Input("data_added_close", "n_clicks")])
def display_table(n1):
    credentials = service_account.Credentials.from_service_account_file('crud.json')
    project_id = 'data-streaming-368616'
    df_sql = f"""SELECT
                 DateTime,
                 Country,
                 Product,
                 Sales,
                 Quantity
                 FROM
                 `data-streaming-368616.crudDatabase.crudTable`
                 ORDER BY
                 DateTime DESC
                 """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df3['DateTime'] = pd.to_datetime(df3['DateTime'])
    df3['DateTime'] = pd.to_datetime(df3['DateTime'], format='%Y-%m-%d %H:%M:%S')
    # df3['Date'] = df3['DateTime'].dt.date
    # df3['Hour'] = pd.to_datetime(df3['DateTime']).dt.hour
    if n1 >= 0:
        return df3.to_dict('records')
