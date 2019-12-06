from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
import numpy as np
import pandas as pd
from descriptive_stadistics import *

dataset = pd.read_csv("demanda_monto.csv")
demandaset = list(dataset["demanda"])
montoset = list(dataset["monto"])
dataset_normalizada_tipicada = get_valores_tipicos(demandaset, montoset)


def regresion_polinomica(dataset_normalizada_tipicada):

    X = np.reshape(dataset_normalizada_tipicada["X"], (-1, 1))
    Y = dataset_normalizada_tipicada["Y"]
    x_entrenamiento, x_prueba, y_entrenamiento, y_prueba = train_test_split(
        X, Y, test_size=0.2)
    regresion_polinomica = PolynomialFeatures(degree=3)
    x_entrenamiento_transformado = regresion_polinomica.fit_transform(
        x_entrenamiento)
    x_prueba_transformado = regresion_polinomica.fit_transform(x_prueba)
    predictor = linear_model.LinearRegression()
    predictor.fit(x_entrenamiento_transformado, y_entrenamiento)
    y_prediccion = predictor.predict(x_prueba_transformado)

    return dict(
        X_ENTRENAMIENTO=[X[0] for X in x_entrenamiento],
        X_PRUEBA=[X[0] for X in x_prueba],
        Y_ENTRENAMIENTO=y_entrenamiento,
        Y_PRUEBA=y_prueba,
        Y_PREDICCION=y_prediccion)


# print(regresion_polinomica(dataset_normalizada_tipicada))
