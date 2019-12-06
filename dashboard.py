import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import flask
from dash.dependencies import Input, Output, State, ClientsideFunction
from datetime import datetime
import pickle
import copy
import pathlib
import dash
import math
import time
import datetime as dt
import pandas as pd
import numpy as np
import pdfkit
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
from dateutil.relativedelta import relativedelta

from descriptive_stadistics import *
from polinomial_regression import *
from reporter import *
from emailer import *

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
app.title = 'Metropolitano'
server = app.server

# Filters

PERIODO = pd.read_csv("periodos.csv")
DISTRITOS = pd.read_csv("distritos.csv")
MODELO_BUS = pd.read_csv("modelo_bus.csv")
TIPO_BUS = pd.read_csv("tipo_bus.csv")
COLOR_BUS = pd.read_csv("color_bus.csv")
RUTAS = pd.read_csv("rutas.csv")
ESTACIONES = pd.read_csv("estaciones.csv")
TIPO_ESTACION = pd.read_csv("tipo_estacion.csv")
TIPO_TARJETA = pd.read_csv("tipo_tarjeta.csv")

# Adapters


def get_adapter(lista, label_id, value_id):
    return [
        {"label": str(lista[label_id][index]),
         "value": str(lista[value_id][index])}
        for index in range(len(lista))
    ]


distrito_options = get_adapter(DISTRITOS, "nombre", "id")

modelo_bus_options = get_adapter(MODELO_BUS, "nombre", "nombre")

tipo_bus_options = get_adapter(TIPO_BUS, "nombre", "nombre")

color_bus_options = get_adapter(COLOR_BUS, "nombre", "nombre")

ruta_options = get_adapter(RUTAS, "nombre", "id")

estacion_options = get_adapter(ESTACIONES, "nombre", "id")

tipo_estacion_options = get_adapter(TIPO_ESTACION, "nombre", "nombre")

tipo_tarjeta_options = get_adapter(TIPO_TARJETA, "nombre", "nombre")

# Conversiones de fechas para filtro slider

daterange = pd.date_range(start=datetime.strptime(PERIODO["inicio"][0], "%Y-%m-%d").strftime(
    '%Y/%m/%d'), end=datetime.strptime(PERIODO["fin"][0], "%Y-%m-%d").strftime('%Y/%m/%d'), freq='W')


def unix_time_millis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))


def unix_to_datetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime(unix, unit='s')


def get_marks(start, end, nth=100):
    ''' Returns the marks for labeling.
        Every Nth value will be used.
    '''

    result = {}
    for i, date in enumerate(daterange):
        if(i % nth == 1):
            result[unix_time_millis(date)] = str(date.strftime('%Y'))

    return result


# Create app layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("metropolitano_logo.svg"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Servicio de Transporte Público",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Metropolitano Lima Perú", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("GitHub", id="learn-more-button"),
                            href="https://github.com/waltercueva/m1-20192-g3",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Periodo",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id='rangeslider_fecha',
                            updatemode='mouseup',
                            min=unix_time_millis(daterange.min()),
                            max=unix_time_millis(daterange.max()),
                            value=[unix_time_millis(daterange.min()),
                                   unix_time_millis(daterange.max())],
                            marks=get_marks(daterange.min(), daterange.max()),
                            tooltip={"always_visible": False,
                                     "placement": "top"},
                            allowCross=False,
                            className="dcc_control",
                        ),
                        html.Hr(style={"margin-bottom": "10px"}),
                        html.P(
                            "Distritos",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="dropdown_distritos",
                            multi=True,
                            options=distrito_options,
                            className="dcc_control",
                        ),
                        html.P(
                            "Modelo del bus",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="dropdown_modelo_bus",
                            multi=True,
                            options=modelo_bus_options,
                            className="dcc_control",
                        ),
                        html.P(
                            "Tipo del bus",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="dropdown_tipo_bus",
                            multi=True,
                            options=tipo_bus_options,
                            className="dcc_control",
                        ),
                        html.P(
                            "Color del bus",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="dropdown_color_bus",
                            multi=True,
                            options=color_bus_options,
                            className="dcc_control",
                        ),
                        html.P(
                            "Rutas",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="dropdown_rutas",
                            multi=True,
                            options=ruta_options,
                            className="dcc_control",
                        ),
                        html.P(
                            "Estaciones",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="dropdown_estaciones",
                            multi=True,
                            options=estacion_options,
                            className="dcc_control",
                        ),
                        html.P(
                            "Tipo de estación",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="dropdown_tipo_estacion",
                            multi=True,
                            options=tipo_estacion_options,
                            className="dcc_control",
                        ),
                        html.P(
                            "Tarifa",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="dropdown_tipo_tarjeta",
                            multi=True,
                            options=tipo_tarjeta_options,
                            className="dcc_control",
                        ),
                        html.Hr(style={"margin-bottom": "10px"}),
                        html.A(
                            html.Button(
                                "Generar reporte", id="generate_pdf", style=dict(width="100%")),
                            href="static/report.pdf", target="_blank"
                        ),
                        html.Hr(style={"margin-bottom": "10px"}),
                        dcc.Input(id="input_email_password",
                                  type="password", placeholder="Clave de correo", style=dict(width="100%")),
                        dcc.Input(id="input_receiver_email_address",
                                  placeholder="Correo destinatario", value="f.michaell.a.m@gmail.com", style=dict(width="100%", marginTop="5px")),
                        html.A(
                            html.Button(
                                "Enviar correo", id="send_email_report", style=dict(width="100%", marginTop="5px"))
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="scatter3d_ganancias_tiempo")],
                            className="pretty_container"),
                        html.Div(
                            [dcc.Graph(id="scattermapbox_demanda_geo")],
                            className="pretty_container"),
                        html.Div(
                            [dcc.Graph(id="surface_demanda_tiempo")],
                            className="pretty_container"),
                        html.Div(
                            [dcc.Graph(
                                id="scatter_regresion_polinomica_demanda_monto")],
                            className="pretty_container"),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        )
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


@app.callback(
    Output('right-column', 'className'),
    [Input('send_email_report', 'n_clicks'), Input("input_email_password", "value"), Input("input_receiver_email_address", "value")])
def send_email_report(n_clicks, input_email_password, input_receiver_email_address):
    if n_clicks != None and input_email_password and input_receiver_email_address:
        try:
            send_email(input_email_password, input_receiver_email_address)
        except:
            print("An exception occurred")
    return


@app.callback(
    dash.dependencies.Output('mainContainer', 'className'),
    [dash.dependencies.Input('generate_pdf', 'n_clicks')])
def generate_pdf(n_clicks):
    if n_clicks != None:
        pdfkit.from_string(build_report(), 'static/report.pdf')
    return


@app.callback(
    Output("scatter3d_ganancias_tiempo", "figure"),
    [
        Input("rangeslider_fecha", "value")
    ]
)
def scatter3d_ganancias_timpo(rangeslider_fecha):

    GANANCIA_TIEMPO = pd.read_csv("monto_tiempo.csv")

    figure = go.Figure(
        data=[
            go.Scatter3d(
                x=list(GANANCIA_TIEMPO["year"]),
                y=list(GANANCIA_TIEMPO["month"]),
                z=list(GANANCIA_TIEMPO["amount"]),
                mode="markers",
                marker=dict(
                    size=7,
                    color=list(GANANCIA_TIEMPO["amount"]),
                    symbol="circle",
                    colorscale='Viridis',
                    opacity=0.8
                )
            )
        ],
        layout=go.Layout(
            title="Ganancias vs. Tiempo",
            autosize=True,
            margin=dict(l=30, r=30, b=40, t=40),
            hovermode="closest",
            plot_bgcolor="#F9F9F9",
            paper_bgcolor="#F9F9F9",
            scene=dict(
                xaxis=dict(
                    title="Año", showgrid=True, zeroline=False, showticklabels=False),
                yaxis=dict(
                    title="Mes", showgrid=True, zeroline=False, showticklabels=False),
                zaxis=dict(title="Ganancia (S/)", showgrid=True, zeroline=False, showticklabels=False))
        )
    )
    return figure


@app.callback(
    Output("scattermapbox_demanda_geo", "figure"),
    [
        Input("rangeslider_fecha", "value")
    ]
)
def scattermapbox_demanda_geo(rangeslider_fecha):

    DEMANDA_GEO = pd.read_csv("demanda_distrito.csv")

    figure = go.Figure(
        go.Scattermapbox(
            lat=list(DEMANDA_GEO["latitud"]),
            lon=list(DEMANDA_GEO["longitud"]),
            text=list(DEMANDA_GEO["demanda"]),
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=10
            )
        )
    )

    figure.update_layout(
        title="Demanda del servicio",
        autosize=True,
        hovermode='closest',
        margin=dict(l=30, r=30, b=40, t=40),
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        mapbox=go.layout.Mapbox(
            accesstoken="pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w",
            pitch=0,
            bearing=0,
            style="light",
            center=go.layout.mapbox.Center(
                lat=-12.044708,
                lon=-77.042387
            ),
            zoom=10
        )
    )

    return figure


@app.callback(
    Output("surface_demanda_tiempo", "figure"),
    [
        Input("rangeslider_fecha", "value")
    ]
)
def surface_demanda_tiempo(rangeslider_fecha):

    year = [2015, 2016, 2017, 2018, 2019]
    month = [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    demanda2d = [[12776, 14438],
                 [14631, 10195, 14066, 10885, 15945, 13757,
                     9695, 13404, 15276, 16213, 13851, 13482],
                 [14295, 12889, 9267, 14652, 12149, 13980,
                     13073, 12753, 12164, 13974, 9379, 13706],
                 [10703, 11978, 13864, 14739, 13702, 11872,
                     13877, 12624, 13476, 12274, 9713, 12962],
                 [7260, 12678, 10067, 19161, 10737, 13701, 15241, 9576, 11492, 9275, 13909]]

    figure = go.Figure(
        data=[
            go.Surface(
                x=year,
                y=month,
                z=demanda2d,
                showscale=True,
                opacity=0.8
            )
        ]
    )

    figure.update_traces(contours_z=dict(show=True, usecolormap=True,
                                         highlightcolor="limegreen", project_z=True))

    figure.update_layout(title='Demanda del Servicio vs Tiempo', autosize=True,
                         margin=dict(l=30, r=30, b=40, t=40), plot_bgcolor="#F9F9F9",
                         paper_bgcolor="#F9F9F9")

    return figure


@app.callback(
    Output("scatter_regresion_polinomica_demanda_monto", "figure"),
    [
        Input("rangeslider_fecha", "value")
    ]
)
def scatter_regresion_polinomica_demanda_monto(rangeslider_fecha):

    dataset = pd.read_csv("demanda_monto.csv")
    demandaset = list(dataset["demanda"])
    montoset = list(dataset["monto"])
    dataset_normalizada_tipicada = get_valores_tipicos(demandaset, montoset)
    result = regresion_polinomica(dataset_normalizada_tipicada)

    figure = go.Figure()

    figure.add_trace(go.Scatter(
        x=result["X_ENTRENAMIENTO"], y=result["Y_ENTRENAMIENTO"], mode='markers', name='Entrenamiento'))
    figure.add_trace(go.Scatter(
        x=result["X_PRUEBA"], y=result["Y_PRUEBA"], mode='markers', name='Prueba'))
    figure.add_trace(go.Scatter(
        x=result["X_PRUEBA"], y=result["Y_PREDICCION"], mode='markers', name='Prediccion', marker_size=10))
    figure.update_layout(
        title="Proyección - Monto recaudado vs Demanda del servicio",
        autosize=True,
        hovermode='closest',
        margin=dict(l=30, r=30, b=40, t=40),
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9"
    )

    return figure


# Main
if __name__ == "__main__":
    app.run_server()
