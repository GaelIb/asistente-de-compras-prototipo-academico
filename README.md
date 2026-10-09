# IKEA AI Experience

Prototipo educativo en Python y Streamlit con catálogo visual, simulación de riesgo de abandono, asistente virtual, pasos ilustrativos de armado y dashboard de demostración. No es una tienda oficial ni está conectado a inventarios, pagos o pedidos.

## Ejecutar en Windows

Probado con Python 3.14.4. Desde esta carpeta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

También puedes ejecutar `iniciar.ps1`, que crea el entorno, instala las dependencias y arranca la aplicación. Abre http://localhost:8501.

## Asistente virtual (opcional)

Copia `.streamlit/secrets.example.toml` como `.streamlit/secrets.toml` y completa `OPENAI_API_KEY`, o define la variable de entorno del mismo nombre. La clave nunca debe subirse al repositorio. El chat usa `gpt-4.1-mini` y requiere una cuenta de API con acceso y saldo. Las otras secciones funcionan sin clave.

## Modelo y alcance de los resultados

`modelo_abandono_rf.pkl` es el modelo incluido en el proyecto original. Solo carga archivos de modelo de origen confiable: joblib/pickle puede ejecutar código.

El entrenamiento usa ocho variables de compras y una etiqueta heurística: más de 90 días sin comprar y menos de cinco compras históricas. Eso aproxima inactividad del cliente, no abandono observado de un carrito. Las reglas del carrito ajustan el resultado entre 0 y 100; el índice no es una probabilidad calibrada. Las métricas del dashboard son datos fijos de demostración.

Para regenerar los datos y entrenar, coloca el archivo original `Online Retail.xlsx` junto al código y ejecuta:

```powershell
python preparar_datos.py
python entrenar_modelo_rf.py
```

El Excel y los CSV de clientes permanecen locales y están excluidos de Git, al igual que la versión histórica `app_viejo.py`, los entornos y las credenciales. El modelo incluido permite ejecutar la aplicación sin esos datasets. `entrenar_modelo.py` conserva el experimento anterior y requiere `datos_abandono.csv` local.

## Verificación

```powershell
python -m unittest discover -s tests -v
```

Las pruebas recorren las seis páginas, los tres perfiles de carrito, las cantidades, los límites del riesgo, los productos de armado y los errores de modelo y chat. No realizan llamadas reales a OpenAI.

Las imágenes y marcas provienen del proyecto original; este repositorio no otorga derechos sobre recursos de terceros.
