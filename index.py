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

    dcc.Interval(id='update_value',
                 interval=1 * 1000,
                 n_intervals=0),

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
                    html.Div('Last data update time:',
                             className='location'),

                    dbc.Spinner(html.Div(id='date',
                                         className='date_id'))
                ], className='location_date_time')
            ], className='nav_title'),

            dbc.Nav([dbc.NavItem(dbc.NavLink('Analyze Data', href='/apps/analyze_data',
                                             active='exact',
                                             style={'color': 'white'})
                                 ),
                     dbc.NavItem(dbc.NavLink('Add Data', href='/apps/add_data',
                                             active='exact',
                                             style={'color': 'white'})
                                 ),
                     dbc.NavItem(dbc.NavLink('User Data', href='/apps/user_data',
                                             active='exact',
                                             style={'color': 'white'})
                                 )

                     ],
                    pills=True,
                    class_name='move_left'
                    ),
        ], className='nav_items')

    ],
        color='dark',
        dark=True,
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


if __name__ == '__main__':
    app.run_server(debug=True)
