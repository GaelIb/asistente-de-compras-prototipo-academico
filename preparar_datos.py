from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

import pandas as pd
from sklearn.preprocessing import LabelEncoder

print("Cargando dataset...")

# =====================================
# CARGAR DATOS
# =====================================

datos = pd.read_excel(
    BASE_DIR / "Online Retail.xlsx",
    engine="openpyxl"
)

print(f"Registros originales: {len(datos)}")

# =====================================
# LIMPIEZA
# =====================================

datos = datos[
    ~datos["InvoiceNo"]
    .astype(str)
    .str.startswith("C")
]

datos = datos[
    datos["Quantity"] > 0
]

datos = datos[
    datos["UnitPrice"] > 0
]

datos = datos.dropna(
    subset=["CustomerID"]
)

print(
    f"Registros después de limpieza: {len(datos)}"
)

# =====================================
# VARIABLES AUXILIARES
# =====================================

datos["InvoiceDate"] = pd.to_datetime(
    datos["InvoiceDate"]
)

datos["TotalLinea"] = (
    datos["Quantity"] *
    datos["UnitPrice"]
)

fecha_referencia = datos[
    "InvoiceDate"
].max()

# =====================================
# AGRUPAR POR CLIENTE
# =====================================

clientes = datos.groupby(
    "CustomerID"
).agg(
    compras_historicas=(
        "InvoiceNo",
        "nunique"
    ),
    gasto_total=(
        "TotalLinea",
        "sum"
    ),
    productos_distintos=(
        "StockCode",
        "nunique"
    ),
    total_productos=(
        "Quantity",
        "sum"
    ),
    ultima_compra=(
        "InvoiceDate",
        "max"
    ),
    primera_compra=(
        "InvoiceDate",
        "min"
    ),
    pais=(
        "Country",
        "first"
    )
)

# =====================================
# VARIABLES DERIVADAS
# =====================================

clientes["ticket_promedio"] = (
    clientes["gasto_total"] /
    clientes["compras_historicas"]
)

clientes["productos_por_compra"] = (
    clientes["total_productos"] /
    clientes["compras_historicas"]
)

clientes["valor_promedio_producto"] = (
    clientes["gasto_total"] /
    clientes["total_productos"]
)

clientes["dias_desde_ultima_compra"] = (
    fecha_referencia -
    clientes["ultima_compra"]
).dt.days

clientes["dias_cliente_activo"] = (
    clientes["ultima_compra"] -
    clientes["primera_compra"]
).dt.days

clientes["dias_cliente_activo"] = (
    clientes["dias_cliente_activo"]
    .replace(0, 1)
)

clientes["frecuencia_compra"] = (
    clientes["compras_historicas"] /
    clientes["dias_cliente_activo"]
)

clientes["dias_entre_compras"] = (
    clientes["dias_cliente_activo"]
    /
    clientes["compras_historicas"]
)

# =====================================
# CODIFICAR PAÍS
# =====================================

encoder = LabelEncoder()

clientes["pais_codificado"] = (
    encoder.fit_transform(
        clientes["pais"]
    )
)

# =====================================
# ETIQUETA DE ABANDONO
# =====================================

clientes["abandono"] = (
    (
        clientes[
            "dias_desde_ultima_compra"
        ] > 90
    )
    &
    (
        clientes[
            "compras_historicas"
        ] < 5
    )
).astype(int)

# =====================================
# LIMPIEZA FINAL
# =====================================

clientes = clientes.reset_index()

print("\nColumnas generadas:")

for columna in clientes.columns:
    print(columna)

clientes.to_csv(
    BASE_DIR / "clientes_ml.csv",
    index=False
)

print("\nDataset generado correctamente")

print(clientes.head())

print(
    f"\nClientes finales: {len(clientes)}"
)