from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq as pd1
import csv

# Connect to main app.py file
from app import app
from app import server

# Connect to your pages
from apps import analyze_data, add_data, user_data

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),

    dcc.Dropdown(
        id='select_product',
        options=['Bread', 'Eggs', 'Yogurt', 'Coconut cream'],
        searchable=True,
        clearable=True,
        style={'margin-top': '-5px',
               'width': '190px',
               'display': 'None'}),

    dbc.Navbar(children=[
        html.Div([
            html.Div([
                html.A(
                    dbc.Row([
                        html.Div([
                            dbc.Col(html.Img(src=app.get_asset_url('statistics.png'), height='30px')),
                            dbc.Col(dbc.NavbarBrand('CRUD App', className='ms-2')),
                        ], className='adjust_image_title')
                    ],
                        align='center',
                        className='g-0',
                    ),
                    href='/apps/outside',
                    style={'textDecoration': 'none'},
                ),

                html.Div([
                    html.Div('Last sales data update time:',
                             className='location'),

                    dbc.Spinner(html.Div(id='date',
                                         className='date_id'),
                                color='success')
                ], className='location_date_time')
            ], className='nav_title'),

            dbc.Nav([dbc.NavItem(dbc.NavLink('Analyze Data', href='/apps/analyze_data',
                                             active='exact',
                                             style={'color': 'white'},
                                             class_name='nav_text_size')
                                 ),
                     dbc.NavItem(dbc.NavLink('Add Sales Data', href='/apps/add_data',
                                             active='exact',
                                             style={'color': 'white'},
                                             class_name='nav_text_size')
                                 ),
                     dbc.NavItem(dbc.NavLink('User Data', href='/apps/user_data',
                                             active='exact',
                                             style={'color': 'white'},
                                             class_name='nav_text_size')
                                 )

                     ],
                    pills=True,
                    class_name='move_left'
                    ),
        ], className='nav_items')

    ],
        color='dark',
        dark=True
    ),

    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/analyze_data':
        return analyze_data.layout
    elif pathname == '/apps/add_data':
        return add_data.layout
    elif pathname == '/apps/user_data':
        return user_data.layout
    else:
        return analyze_data.layout


@app.callback(Output('date', 'children'),
              [Input('select_product', 'value')])
def update_confirmed(n_intervals):
    credentials = service_account.Credentials.from_service_account_file('crud.json')
    project_id = 'data-streaming-368616'
    df_sql = f"""SELECT DateTime
                     FROM
                     `data-streaming-368616.crudDatabase.crudTable`
                     ORDER BY
                     DateTime DESC LIMIT 1
                     """
    df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    get_date = df['DateTime'].head(1).iloc[0]

    return [
        html.Div(get_date,
                 className='date_format')
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
