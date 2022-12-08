# This file is a dash app. Read more about dash here: https://dash.plotly.com/
# Please add to this file to customize your incubator!

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import sqlite3

app = Dash(__name__)

# Connect to database
conn = sqlite3.connect("lucas-test.db")
cursor = conn.cursor()

# Read previous 1 week of data
# TODO: set an app.layout function to reload data on page load
# See https://dash.plotly.com/basic-callbacks
df = pd.read_sql_query("""
  SELECT datetime(time_sec, 'unixepoch', 'localtime') as time, temp, humidity from temp_humid_1m
  WHERE time_sec > strftime('%s', datetime('now', '-6 days'))
  ORDER BY time_sec DESC
  """, conn)

temp = px.line(df, x="time", y="temp", title="Temperature")
humidity = px.line(df, x="time", y="humidity", title="Humidity")


app.layout = html.Div(children=[
    html.H1(children='piano-bench admin'),

    # TODO: get incubator name from environment
    html.Div(children='''
        Welcome to piano-bench
    '''),

    dcc.Graph(
        id='temp',
        figure=temp
    ),

    dcc.Graph(
        id='humidity',
        figure=humidity
    )
])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
