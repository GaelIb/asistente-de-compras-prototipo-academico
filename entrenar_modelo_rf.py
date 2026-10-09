from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

print(
    "Cargando dataset preparado..."
)

datos = pd.read_csv(
    BASE_DIR / "clientes_ml.csv"
)

# =====================================
# FEATURES
# =====================================

X = datos[
    [
        "compras_historicas",
        "gasto_total",
        "productos_distintos",
        "total_productos",
        "ticket_promedio",
        "productos_por_compra",
        "valor_promedio_producto",
        "dias_entre_compras"
    ]
]

# =====================================
# TARGET
# =====================================

y = datos["abandono"]

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
)

# =====================================
# MODELO
# =====================================

modelo = RandomForestClassifier(
    n_estimators=500,
    max_depth=12,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

print(
    "Entrenando modelo..."
)

modelo.fit(
    X_train,
    y_train
)

# =====================================
# EVALUACIÓN
# =====================================

predicciones = modelo.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predicciones
)

print("\nAccuracy:")

print(
    f"{accuracy:.4f}"
)

print("\nMatriz de confusión:")

print(
    confusion_matrix(
        y_test,
        predicciones
    )
)

print("\nReporte:")

print(
    classification_report(
        y_test,
        predicciones
    )
)

# =====================================
# IMPORTANCIA VARIABLES
# =====================================

print(
    "\nImportancia de variables:\n"
)

for nombre, importancia in zip(
    X.columns,
    modelo.feature_importances_
):

    print(
        f"{nombre}: {importancia:.4f}"
    )

# =====================================
# GUARDAR
# =====================================

joblib.dump(
    modelo,
    BASE_DIR / "modelo_abandono_rf.pkl"
)

print(
    "\nModelo guardado correctamente."
)