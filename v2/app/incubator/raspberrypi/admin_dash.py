# This file is a dash app. Read more about dash here: https://dash.plotly.com/
# Please add to this file to customize your incubator!

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import subprocess

app = Dash(__name__)


app.layout = html.Div(children=[
    html.H1(children='piano-bench admin'),

    # TODO: get incubator name from environment
    html.Div(children='''
        Welcome to piano-bench
    '''),
    html.Div(id='interval-updated-graphs'),
    # This component is used to refresh data in the background because it was
    # too slow when rendering while serving a request. See `@app.callback` below
    dcc.Interval(
        id='interval-component',
        interval=10 * 60 * 1000,  # ten minutes in milliseconds
        n_intervals=0
    )
])


def get_current_user():
    return subprocess.check_output(
        'whoami', shell=True).decode("utf-8").strip()


def get_database_conn_and_cursor():
    conn = sqlite3.connect(f"/home/{get_current_user()}/incubator.db")
    cursor = conn.cursor()
    return (conn, cursor)


@app.callback(Output('interval-updated-graphs', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(_):
    (conn, _) = get_database_conn_and_cursor()
    # Read previous 1 week of data
    df = pd.read_sql_query("""
SELECT datetime(time_sec, 'unixepoch', 'localtime') as time, temp, humidity from temp_humid_1m
WHERE time_sec > strftime('%s', datetime('now', '-1 month'))
ORDER BY time_sec DESC
""", conn)

    temp = px.line(df, x="time", y="temp", title="Temperature")
    humidity = px.line(df, x="time", y="humidity", title="Humidity")

    return [dcc.Graph(id='temp', figure=temp), dcc.Graph(id='humidity', figure=humidity)]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
