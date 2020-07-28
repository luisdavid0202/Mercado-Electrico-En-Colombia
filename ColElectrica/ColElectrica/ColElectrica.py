import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm

db = pd.read_csv("data.csv", index_col="FECHA")
db = db.sort_index()
db.index = pd.to_datetime(db.index, format='%Y%m%d')

db3 = db[db["DEPARTAMENTO"] == "ANTIOQUIA"]
db3 = db3[db3["MUNICIPIO"] == "MEDELLIN"]
db3 = db3[db3["AGENTE"] == "EMPRESAS PUBLICAS DE MEDELLIN ESP"]
db3 = db3[db3["NIVEL TENSION"] == 1]
db3 = db3.asfreq('M')

samples = db3["2010-09-01":"2020-01-30"]["DEMANDA"]
train = samples.loc["2010-09-01":"2019-01-30"]
test = samples.loc["2019-01-30":"2020-01-30"]

ciclo, trend = sm.tsa.filters.hpfilter(db3["2010-09-01":"2020-01-30"]["DEMANDA"])


# Autocorrelacion da P
p = 5

# Autocorrelacion parcial da Q
q = 5

# Trend
d = 2

sarima = SARIMAX(train, order=(p,d,q), seasonal_order=(p, d, q, 12))
sarima_fit = sarima.fit(disp=0)

forecast = sarima_fit.forecast(12)

data = {'forecast': forecast, 'test': list(test), 'date': test.index}

app = dash.Dash()

app.layout = html.Div(
    children=[
        html.H1(children="Electricity consumption"),

        dcc.Graph(
            id="ejemplo",
            figure={
                "data": [
                    {
                        "x": (db3["2010-09-01":"2020-01-30"].index),
                        "y": db3["2010-09-01":"2020-01-30"]["DEMANDA"].tolist(),
                        "type": "line",
                        "name": "Electricity consumption",
                    },
                    {
                        "x": (db3["2010-09-01":"2020-01-30"].index),
                        "y": pd.Series(db3["2010-09-01":"2020-01-30"]["DEMANDA"]).rolling(window=12).mean(),
                        "type": "line",
                        "name": "Moving average",
                    },
                    {
                        "x": (db3["2010-09-01":"2020-01-30"].index),
                        "y": pd.Series(db3["2010-09-01":"2020-01-30"]["DEMANDA"]).rolling(window=12).std(),
                        "type": "line",
                        "name": "Standart Dev",
                    },   
                    {
                        "x": (db3["2010-09-01":"2020-01-30"].index),
                        "y": trend,
                        "type": "line",
                        "name": "Trend",
                    },                   
                ],
                "layout": {"title": "Electricity consumption Medellin, Antioquia. Date: 2010-09-01, 2020-01-30"},
            },
        ),


        dcc.Graph(
            id="ejemplo1",
            figure={
                "data": [
                    {
                        "x": data["date"],
                        "y": data["forecast"],
                        "type": "line",
                        "name": "Forecast values",
                    },
                    {
                        "x": data["date"],
                        "y": data["test"],
                        "type": "line",
                        "name": "Test values",
                    },
                ],
                "layout": {"title": "Forecast values VS Test values"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
