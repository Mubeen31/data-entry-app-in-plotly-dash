from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from app import app
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq as pd1

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
print(sales_by_product)
