from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from app import app
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq as pd1

sales_by_product_chart = dcc.Graph(id='bar_chart',
                                   config={'displayModeBar': False},
                                   className='tab_bar_chart'),
sales_by_country_chart = dcc.Graph(id='bubble_chart',
                                   config={'displayModeBar': False},
                                   className='tab_bar_chart')

tab_style = {
    'border-top': 'none',
    'border-bottom': 'none',
    'border-left': 'none',
    'border-right': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)',
    'height': '35px',
    'padding': '7.5px',
    'width': 'auto'
}

selected_tab_style = {
    'border-top': 'none',
    'border-bottom': '2px solid blue',
    'border-left': 'none',
    'border-right': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)',
    'height': '35px',
    'padding': '7.5px',
    'width': 'auto'
}

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
    ], className='card_row'),

    html.Div([
        html.Div([
            dcc.Graph(id='line_chart',
                      config={'displayModeBar': False})
        ], className='first_chart'),

        html.Div([
            dcc.Tabs(value='sales_by_product_chart', children=[
                dcc.Tab(sales_by_product_chart,
                        label='Sales by Product',
                        value='sales_by_product_chart',
                        style=tab_style,
                        selected_style=selected_tab_style),
                dcc.Tab(sales_by_country_chart,
                        label='Sales by Country',
                        value='sales_by_country_chart',
                        style=tab_style,
                        selected_style=selected_tab_style)
            ], style={'display': 'flex', 'flex-direction': 'row'})
        ], className='tabs_container')
    ], className='first_chart_grid'),

    html.Div(id='return_tab_content', children=[])
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
    total_sales = len(str(df3['Sales'].sum()))
    total_sales_million = df3['Sales'].sum() / 1000000
    total_sales_billion = df3['Sales'].sum() / 1000000000
    total_sales_trillion = df3['Sales'].sum() / 1000000000000

    if total_sales >= 0 and total_sales <= 7:
        return [
            html.Div('Total Sales',
                     style={'color': '#a6a6a6',
                            'margin-left': '10px',
                            'margin-top': '5px'}),
            html.Div([
                html.Div('{0:,.3f} M'.format(total_sales_million),
                         className='numeric_value'),
                html.Div('$', className='symbol')
            ], className='numeric_value_center')
        ]
    elif total_sales >= 8 and total_sales <= 10:
        return [
            html.Div('Total Sales',
                     style={'color': '#a6a6a6',
                            'margin-left': '10px',
                            'margin-top': '5px'}),
            html.Div([
                html.Div('{0:,.3f} B'.format(total_sales_billion),
                         className='numeric_value'),
                html.Div('$', className='symbol')
            ], className='numeric_value_center')
        ]
    elif total_sales >= 11:
        return [
            html.Div('Total Sales',
                     style={'color': '#a6a6a6',
                            'margin-left': '10px',
                            'margin-top': '5px'}),
            html.Div([
                html.Div('{0:,.3f} T'.format(total_sales_trillion),
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


@app.callback(Output('line_chart', 'figure'),
              [Input('update_data', 'n_intervals')])
def update_value(n_intervals):
    credentials = service_account.Credentials.from_service_account_file('crud.json')
    project_id = 'data-streaming-368616'
    df_sql = f"""SELECT
                     DateTime,
                     Sales
                     FROM
                     `data-streaming-368616.crudDatabase.crudTable`
                     ORDER BY DateTime
                     """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df3 = df3.dropna(how='any', axis=0)

    return {
        'data': [go.Scatter(
            x=df3['DateTime'].tail(15),
            y=df3['Sales'].tail(15),
            mode='markers+lines',
            line=dict(width=3, color='rgb(214, 32, 32)'),
            marker=dict(size=7, symbol='circle', color='rgb(214, 32, 32)',
                        line=dict(width=2, color='rgb(214, 32, 32)')),
            hoverinfo='text',
            hovertext=
            '<b>Date Time</b>: ' + df3['DateTime'].tail(15).astype(str) + '<br>' +
            '<b>Sales ($)</b>: ' + [f'{x:.3f} $' for x in df3['Sales'].tail(15)] + '<br>'
        )],
        'layout': go.Layout(
            height=350,
            title={'text': '<b>Current Sales</b>',
                   'y': 0.95,
                   'x': 0.5,
                   'yanchor': 'top',
                   'xanchor': 'center'},
            titlefont={'color': 'rgb(214, 32, 32)',
                       'size': 17},
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            hovermode='x',
            margin=dict(t=50, l=50, r=40),
            xaxis=dict(
                showline=True,
                showgrid=False,
                linecolor='#666666',
                linewidth=1,
                ticks='outside',
                color='#666666',
                tickfont=dict(family='Arial',
                              size=12,
                              color='#666666')
            ),
            yaxis=dict(
                # range=[min(df3['Sales']) - 0.05, max(df3['Sales']) + 0.05],
                zeroline=False,
                showline=False,
                showgrid=True,
                gridcolor='#e6e6e6',
                color='#666666',
                tickfont=dict(family='Arial',
                              size=12,
                              color='#666666')
            )
        )
    }


@app.callback(Output('bar_chart', 'figure'),
              [Input('update_data', 'n_intervals')])
def update_value(n_intervals):
    credentials = service_account.Credentials.from_service_account_file('crud.json')
    project_id = 'data-streaming-368616'
    df_sql = f"""SELECT
                     Product,
                     Sales,
                     Quantity
                     FROM
                     `data-streaming-368616.crudDatabase.crudTable`
                     """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df3 = df3.dropna(how='any', axis=0)
    sales_by_product = df3.groupby(['Product']).agg({'Sales': 'sum', 'Quantity': 'sum'}).reset_index()

    return {
        'data': [go.Bar(
            x=sales_by_product['Product'],
            y=sales_by_product['Sales'],
            marker=dict(color=sales_by_product['Sales'],
                        colorscale='HSV',
                        showscale=False,
                        ),
            hoverinfo='text',
            hovertext=
            '<b>Product</b>: ' + sales_by_product['Product'].astype(str) + '<br>' +
            '<b>Sales ($)</b>: ' + [f'{x:.3f} $' for x in sales_by_product['Sales']] + '<br>' +
            '<b>Quantity</b>: ' + [f'{x:.0f}' for x in sales_by_product['Quantity']] + '<br>'
        )],
        'layout': go.Layout(
            height=350,
            title={'text': '<b>Sales by Product</b>',
                   'y': 0.95,
                   'x': 0.5,
                   'yanchor': 'top',
                   'xanchor': 'center'},
            titlefont={'color': 'rgb(214, 32, 32)',
                       'size': 17},
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            hovermode='x',
            margin=dict(t=50, l=50, r=40),
            xaxis=dict(
                showline=True,
                showgrid=False,
                linecolor='#666666',
                linewidth=1,
                ticks='outside',
                color='#666666',
                tickfont=dict(family='Arial',
                              size=12,
                              color='#666666')
            ),
            yaxis=dict(showline=False,
                       showgrid=True,
                       gridcolor='#e6e6e6',
                       color='#666666',
                       tickfont=dict(family='Arial',
                                     size=12,
                                     color='#666666')
                       )
        )
    }


@app.callback(Output('bubble_chart', 'figure'),
              [Input('update_data', 'n_intervals')])
def update_value(n_intervals):
    credentials = service_account.Credentials.from_service_account_file('crud.json')
    project_id = 'data-streaming-368616'
    df_sql = f"""SELECT
                     Country,
                     Sales,
                     Quantity
                     FROM
                     `data-streaming-368616.crudDatabase.crudTable`
                     """
    df3 = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df3 = df3.dropna(how='any', axis=0)
    sales_by_product = df3.groupby(['Country']).agg({'Sales': 'sum', 'Quantity': 'sum'}).reset_index()

    return {
        'data': [go.Scatter(
            x=sales_by_product['Country'],
            y=sales_by_product['Sales'],
            text=sales_by_product['Country'],
            textposition='top center',
            mode='markers + text',
            marker=dict(size=sales_by_product['Sales'].astype(int) / 25,
                        color=sales_by_product['Sales'],
                        colorscale='HSV',
                        showscale=False,
                        line=dict(
                            color='MediumPurple',
                            width=2
                        )),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + sales_by_product['Country'].astype(str) + '<br>' +
            '<b>Sales ($)</b>: ' + [f'{x:.3f} $' for x in sales_by_product['Sales']] + '<br>' +
            '<b>Quantity</b>: ' + [f'{x:.0f}' for x in sales_by_product['Quantity']] + '<br>'
        )],
        'layout': go.Layout(
            height=350,
            title={'text': '<b>Sales by Country</b>',
                   'y': 0.95,
                   'x': 0.5,
                   'yanchor': 'top',
                   'xanchor': 'center'},
            titlefont={'color': 'rgb(214, 32, 32)',
                       'size': 17},
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            hovermode='x',
            margin=dict(t=50, l=50, r=40),
            xaxis=dict(
                showline=True,
                showgrid=False,
                linecolor='#666666',
                linewidth=1,
                ticks='outside',
                color='#666666',
                tickfont=dict(family='Arial',
                              size=12,
                              color='#666666')
            ),
            yaxis=dict(zeroline=False,
                       showline=False,
                       showgrid=True,
                       gridcolor='#e6e6e6',
                       color='#666666',
                       tickfont=dict(family='Arial',
                                     size=12,
                                     color='#666666')
                       )
        )
    }
