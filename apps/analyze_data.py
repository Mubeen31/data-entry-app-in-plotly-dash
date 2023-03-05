from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from app import app
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq as pd1

layout = html.Div([])