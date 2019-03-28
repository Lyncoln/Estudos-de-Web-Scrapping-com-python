from datetime import datetime
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import psutil
import plotly.graph_objs as go
from collections import deque

X = deque(maxlen=40)
Y = deque(maxlen=40)
X.append(datetime.now())
Y.append(psutil.cpu_percent())

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-update-graph', animate=False),
        dcc.Interval(
            id='interval-component',
            interval=1000,
            n_intervals=0
            )
        ]
    )

@app.callback(Output('live-update-graph', 'figure'),
        [Input('interval-component', 'n_intervals')])
def update_graph(n):
    tempo = datetime.now()
    X.append(tempo )
    Y.append(psutil.cpu_percent())

    data = go.Scatter(
        x = list(X),
        y = list(Y),
        name = 'Scatter',
        mode = 'lines+markers'
        )

    return {'data':[data], 'layout': go.Layout(xaxis = dict(autorange=True),
                                               yaxis = dict(range=[0, 100]))}

if __name__ == '__main__':
    app.run_server(debug=True)