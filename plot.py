import dash
from dash.dependencies import Output, Input, State
from dash import dcc
from dash import html
import plotly
import plotly.graph_objs as go
from time_to_alarm import AlarmTime

from consumer import SensorsUpdater
from kafka_producer import KafkaProducer

ARR_SIZE = 200
MAX_Y = 60

c = 0
val_y = 0
prev_size = 0

sent = True

app = dash.Dash(__name__)
sensor_updater = SensorsUpdater("sensors", ["192.168.88.241:9092"])
sensor_updater.endless_consume()
producer = KafkaProducer("192.168.88.241:9092")

@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals'), Input("input_{}".format("text"), "value")],
)
def update_graph_scatter(n, input_time):
    global prev_size
    global sent

    if input_time is not None and len(input_time) == 5 and sent:
        producer.send_msg(AlarmTime(input_time).to_JSON(), "topic_2")
        print("Send new time to topic 2", sent, len(input_time))
        sent = False

    if input_time is not None:
        print(len(input_time))

    if input_time is not None and len(input_time) != 5:
        print("Len != 5")
        sent = True

    if prev_size != len(sensor_updater.arr_of_vals_of_sensor):
        # print("New element plotting...")

        global yy
        global c
        global val_y

        if len(X) >= ARR_SIZE:
            X[c] = c
            Y[c] = sensor_updater.arr_of_vals_of_sensor[prev_size]
            X_humidity[c] = c
            Y_humidity[c] = sensor_updater.arr_of_vals_of_sensor_humidity[prev_size]
            c += 1
            if c == ARR_SIZE - 1:
                c = 0
        else:
            X.append(X[-1] + 1)
            X_humidity.append(X[-1] + 1)
            val_y = sensor_updater.arr_of_vals_of_sensor[prev_size]
            Y.append(val_y)
            Y_humidity.append(sensor_updater.arr_of_vals_of_sensor_humidity[prev_size])
            if len(X) < ARR_SIZE / 2:
                val_y += 1
            else:
                val_y -= 1

        prev_size = len(sensor_updater.arr_of_vals_of_sensor)

    data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers',
    )

    data2 = plotly.graph_objs.Scatter(
        x=list(X_humidity),
        y=list(Y_humidity),
        name='Scatter',
        mode='lines+markers',
    )

    return {'data': [data, data2],
            'layout': go.Layout(xaxis=dict(range=[0, ARR_SIZE]), yaxis=dict(range=[0, MAX_Y]), )}


if __name__ == '__main__':
    X = [0]
    Y = [0]

    X_humidity = [0]
    Y_humidity = [0]

    app.layout = html.Div(
        [
            dcc.Graph(id='live-graph', animate=False),
            dcc.Interval(
                id='graph-update',
                interval=900,
            ),
            # html.Button('Submit', id='submit-val', n_clicks=0),
            dcc.Input(
                id="input_{}".format("text"),
                type="text",
                placeholder="input type {}".format("text"),
            ),
            # html.Button('Submit', id='submit-val', n_clicks=0),
        ]
    )

    app.run_server(host="192.168.88.241", port=8080)