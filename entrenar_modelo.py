from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# entrenar_modelo.py

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

datos = pd.read_csv(BASE_DIR / "datos_abandono.csv")

X = datos[["tiempo","cambios"]]
y = datos["abandono"]

modelo = DecisionTreeClassifier()

modelo.fit(X,y)

joblib.dump(modelo,BASE_DIR / "modelo_abandono.pkl")

print("Modelo guardado")