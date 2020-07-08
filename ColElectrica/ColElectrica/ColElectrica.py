import dash
import dash_core_components as dcc
import dash_html_components as html
import flask


server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server
)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    children=[
        html.H1(children="Demo basico"),

        dcc.Graph(
            id="ejemplo",
            figure={
                "data": [
                    {
                        "x": [1, 2, 3, 4],
                        "y": [1, 8, 3, 7],
                        "type": "line",
                        "name": "Bicicletas",
                    },
                    {
                        "x": [1, 2, 3, 4],
                        "y": [5, 2, 8, 8],
                        "type": "bar",
                        "name": "bicicletas electricas",
                    },
                ],
                "layout": {"title": "Ejemplo básico Dash"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=4500)
