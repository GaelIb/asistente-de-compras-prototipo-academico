import streamlit as st
import os
from pathlib import Path
import pandas as pd
import joblib
import plotly.express as px
from openai import OpenAI
from analytics import ajustar_riesgo

BASE_DIR = Path(__file__).resolve().parent


def recurso(nombre):
    return str(BASE_DIR / nombre)


# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="IKEA Customer Analytics AI",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# ESTILOS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 1rem;
}

h1 {
    color: #0058A3;
}

.metric-container {
    background-color: white;
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# OPENAI
# =====================================================

api_key = os.environ.get("OPENAI_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        pass
client = OpenAI(api_key=api_key, timeout=30.0, max_retries=1) if api_key else None
openai_ok = client is not None

# =====================================================
# MODELO
# =====================================================

@st.cache_resource
def cargar_modelo():
    return joblib.load(BASE_DIR / "modelo_abandono_rf.pkl")


# =====================================================
# FUNCIONES
# =====================================================

def mostrar_inicio():

    st.image(
        recurso("IKEAPNG.png"),
        width="stretch"
    )
    st.title(
        "IKEA AI Experience"
    )

    st.write(
        "Experiencia personalizada impulsada por Inteligencia Artificial."
    )

    st.subheader(
        "Productos recomendados"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.image(
            recurso("imagenes-sofa.jpg"),
            width="stretch"
        )

        st.subheader(
            "LINANÄS"
        )

        st.write("$250")

    with c2:

        st.image(
            recurso("imagenes-mesa.jpg"),
            width="stretch"
        )

        st.subheader(
            "LISABO"
        )

        st.write("$300")

    with c3:

        st.image(
            recurso("imagenes-silla.jpg"),
            width="stretch"
        )

        st.subheader(
            "ODGER"
        )

        st.write("$60")

def mostrar_chat():

    st.title(
        "Asistente Virtual IKEA"
    )

    st.write(
        "Haz preguntas sobre productos, decoración y mobiliario."
    )

    pregunta = st.chat_input(
        "Escribe tu pregunta..."
    )

    if pregunta:

        st.chat_message(
            "user"
        ).write(
            pregunta
        )

        if openai_ok:

            with st.spinner(
                "Consultando asistente..."
            ):

                try:

                    respuesta = client.chat.completions.create(

                        model="gpt-4.1-mini",

                        messages=[

                            {
                                "role": "system",
                                "content":
                                """
                                Eres un asesor experto de IKEA.

                                    Productos disponibles en esta tienda:

                                    LINANÄS:
                                    Sofá de 3 plazas,
                                    ideal para espacios medianos.

                                    LISABO:
                                    Mesa de madera de estilo nórdico.

                                    ODGER:
                                    Silla ergonómica para comedor
                                    y oficina.

                                    FADO:
                                    Lámpara decorativa.

                                    TIPHEDE:
                                    Alfombra moderna para sala.

                                    Responde utilizando estos productos
                                    cuando sea apropiado.
                                    """
                                },

                            {
                                "role": "user",
                                "content": pregunta
                            }

                        ]

                    )

                    respuesta_gpt = (
                        respuesta
                        .choices[0]
                        .message
                        .content
                    )

                    st.chat_message(
                        "assistant"
                    ).write(
                        respuesta_gpt
                    )

                except Exception:

                    st.error(
                        "No se pudo consultar el asistente. Revisa la clave de API, el saldo y la conexión."
                    )

        else:

            st.warning(
                "No se detectó OPENAI_API_KEY."
            )


def mostrar_privacidad():

    st.title(" Ética y Privacidad")

    st.write("""
    Esta demostración usa perfiles de cliente y controles simulados.
    No registra navegación ni realiza compras.

    Al usar el asistente virtual, tu pregunta y el contexto del catálogo
    se envían a OpenAI para generar una respuesta.
    Evita incluir datos personales o información confidencial.
    """)

def mostrar_carrito():

    st.title("Carrito Inteligente")

    st.write(
        "Sistema predictivo para detección de abandono de compra."
    )
    st.caption("Simulación: combina un modelo de inactividad de clientes con reglas de comportamiento. El resultado es un índice orientativo de riesgo, no una probabilidad validada de abandono del carrito.")
    try:
        modelo = cargar_modelo()
    except (FileNotFoundError, ValueError, ImportError, EOFError):
        st.error("No se pudo cargar el modelo. Ejecuta python entrenar_modelo_rf.py con los datos de entrenamiento disponibles.")
        return

    st.divider()

    col1, col2 = st.columns([2,1])

    with col1:

        st.subheader("Mi carrito")

        st.image(
            recurso("imagenes-sofa.jpg"),
            width=250
        )

        st.write("LINANÄS")
        st.write("$250")
        cantidad_sofa = st.number_input(
            "Cantidad LINANÄS",
            min_value=1,
            value=1,
            key="sofa"
       )

        st.divider()

        st.image(
            recurso("imagenes-mesa.jpg"),
            width=250
        )

        st.write("LISABO")
        st.write("$300")
        cantidad_mesa = st.number_input(
            "Cantidad LISABO",
            min_value=1,
            value=1,
            key="mesa"
        )

        st.divider()

        subtotal=(
            cantidad_sofa * 250
             +
            cantidad_mesa * 300
        )

        st.subheader(
            f"Subtotal: ${subtotal:,.0f}"
                )


    with col2:
        cliente = st.selectbox(
            "Perfil de cliente",
            [
                "Cliente frecuente",
                "Cliente ocasional",
                "Cliente inactivo"
            ]
        )

        if cliente == "Cliente frecuente":
                compras = 15
                gasto = 5000
                productos = 25
                total_productos = 40

                ticket = 300
                productos_compra = 4
                valor_producto = 100
                dias_entre_compras = 20

        elif cliente == "Cliente ocasional":

                compras = 5
                gasto = 1500
                productos = 10
                total_productos = 20

                ticket = 250
                productos_compra = 2
                valor_producto = 90
                dias_entre_compras = 35


        else:

                compras = 1
                gasto = 200
                productos = 3
                total_productos = 5

                ticket = 150
                productos_compra = 1
                valor_producto = 80
                dias_entre_compras = 90


        tiempo_carrito = st.slider(
        "Minutos en el carrito",
        0,
        60,
        15
         )

        productos_vistos = st.slider(
            "Productos vistos",
            1,
            50,
            8
        )

        visitas_recientes = st.slider(
            "Visitas recientes",
            1,
            20,
            4
        )

    analizar = st.button(
        "Analizar Carrito",
        width="stretch"
    )

    if analizar:
        datos_cliente = pd.DataFrame(
            [[
                compras,
                gasto,
                productos,
                total_productos,
                ticket,
                productos_compra,
                valor_producto,
                dias_entre_compras
            ]],
            columns=[
                "compras_historicas",
                "gasto_total",
                "productos_distintos",
                "total_productos",
                "ticket_promedio",
                "productos_por_compra",
                "valor_promedio_producto",
                "dias_entre_compras",
            ]
        )

        probabilidad = modelo.predict_proba(
            datos_cliente
        )[0][1]

        riesgo = ajustar_riesgo(probabilidad, tiempo_carrito, productos_vistos, visitas_recientes)
        st.divider()

        st.metric(
            "Índice de riesgo (simulación)",
            f"{riesgo:.1f}%"
        )
        colA, colB, colC = st.columns(3)

        with colA:

            st.metric(
                "Tiempo en carrito",
                f"{tiempo_carrito} min"
            )

        with colB:

            st.metric(
                "Productos vistos",
                productos_vistos
            )

        with colC:

            st.metric(
                "Visitas recientes",
                visitas_recientes
            )

        st.subheader(
            "Acciones sugeridas por IA"
        )
        if riesgo >= 70:

            acciones = [
                "Generar cupón de descuento del 10%",
                "Consultar disponibilidad antes de informar sobre inventario",
                "Enviar recordatorio de compra"
            ]

            st.error(
                "Riesgo alto de abandono detectado."
            )

            st.info(
                "Ejemplo de acción: comprobar si existe una promoción disponible."
            )

            st.info(
                "Consulta el inventario real antes de mostrar avisos de disponibilidad."
            )

            st.info(
                "Se recomienda ofrecer un descuento del 10%."
            )

            st.info(
                "Mostrar productos complementarios."
            )

            st.success(
                f"Ejemplo con descuento del 10%: subtotal ${subtotal * 0.9:,.2f}."
            )

            st.warning(
                "Esta demostración no está conectada al inventario."
            )

            st.info(
                "Recomendación IA: ofrecer cupón de 10%."
            )


        elif riesgo >= 40:

            acciones = [
                "Mostrar productos relacionados",
                "Enviar notificación de seguimiento"
            ]

            st.warning(
                "Riesgo medio de abandono."
            )

            st.info(
                "Enviar recordatorio de compra."
            )

            st.info(
                "Mostrar recomendaciones personalizadas."
            )

        else:
            acciones = [
                "Recomendar productos complementarios"
            ]
            st.success(
                "Probabilidad alta de completar la compra."
            )
        for accion in acciones:

            st.write(
                "•",
                accion
            )

        st.divider()

        st.subheader(
            "Mensajes personalizados"
        )

        if riesgo >= 70:

            st.warning(
                "Parece que llevas tiempo sin completar tu compra."
            )

            st.info(
                "Consulta las promociones disponibles para tu producto."
            )

            st.success(
                "Ejemplo: ofrecer un cupón si la tienda lo autoriza."
            )

        elif riesgo >= 40:

            st.info(
                "¿Necesitas ayuda para completar tu compra?"
            )

        else:

            st.success(
                "Gracias por comprar con IKEA."
            )
    st.subheader(
        "Productos recomendados"
    )


    c1, c2, c3 = st.columns(3)

    with c1:
        st.image(
            recurso("imagenes-silla.jpg"),
            width="stretch"
        )
        st.write("ODGER")

    with c2:
        st.image(
            recurso("imagenes-lampara.jpg"),
            width="stretch"
        )
        st.write("FADO")

    with c3:
        st.image(
            recurso("imagenes-alfombra.jpg"),
            width="stretch"
        )
        st.write("TIPHEDE")


def mostrar_dashboard():

    st.title("Dashboard IA")
    st.caption("Datos de demostración: las métricas y gráficas siguientes son ejemplos fijos, no resultados de actividad real.")

    st.write(
        "Monitoreo de comportamiento y abandono de clientes."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Clientes Analizados",
            "4,338"
        )

    with col2:
        st.metric(
            "Riesgo Promedio",
            "42%"
        )

    with col3:
        st.metric(
            "Compras Recuperadas",
            "183"
        )

    with col4:
        st.metric(
            "Conversión",
            "78%"
        )

    st.divider()

    df_dashboard = pd.DataFrame({

        "Perfil": [
            "Frecuente",
            "Ocasional",
            "Inactivo"
        ],

        "Abandono": [
            18,
            46,
            81
        ]

    })

    fig = px.bar(

        df_dashboard,

        x="Perfil",

        y="Abandono",

        title="Tasa de abandono por perfil de cliente"

    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


    st.divider()

    df_tendencia = pd.DataFrame({

        "Mes": [
            "Ene",
            "Feb",
            "Mar",
            "Abr",
            "May",
            "Jun"
        ],

        "Abandono": [
            54,
            49,
            45,
            42,
            39,
            35
        ]

    })

    fig2 = px.line(

        df_tendencia,

        x="Mes",

        y="Abandono",

        markers=True,

        title="Tendencia de abandono"

    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )


    st.divider()

    st.subheader(
        "Resumen Ejecutivo"
    )

    resumen = pd.DataFrame({

        "Indicador": [
            "Clientes activos",
            "Clientes en riesgo",
            "Clientes recuperados"
        ],

        "Valor": [
            3380,
            775,
            183
        ]

    })

    st.dataframe(
        resumen,
        width="stretch"
    )


def mostrar_armado():

    st.title("Armado Inteligente")
    st.caption("Demostración con pasos ilustrativos. Consulta el manual oficial del producto para realizar el montaje.")

    st.write(
        "Asistente de ensamblaje asistido por IA."
    )

    producto = st.selectbox(
        "Selecciona un producto",
        [
            "Mesa LISABO",
            "Sofá LINANÄS",
            "Silla ODGER"
        ]
    )

    if producto == "Mesa LISABO":

        st.image(
            recurso("imagenes-mesa.jpg"),
            width=300
        )
        st.progress(25)

        st.success(
            "Producto identificado correctamente."
        )

        st.subheader(
            "Paso 1"
        )

        st.info(
            "Conectar las patas a la base utilizando 4 tornillos tipo A."
        )

    elif producto == "Sofá LINANÄS":

        st.image(
            recurso("imagenes-sofa.jpg"),
            width=300
        )
        st.progress(25)

        st.success(
            "Producto identificado correctamente."
        )

        st.subheader(
            "Paso 1"
        )

        st.info(
            "Fijar los brazos laterales utilizando los pernos incluidos."
        )

    elif producto == "Silla ODGER":

        st.image(
            recurso("imagenes-silla.jpg"),
            width=300
        )

        st.success(
            "Producto identificado correctamente."
        )

        st.subheader(
            "Paso 1"
        )

        st.info(
            "Insertar el respaldo en la base hasta escuchar el clic de seguridad."
        )

        st.progress(25)
# =====================================================
# NAVEGACIÓN
# =====================================================

st.sidebar.image(
    recurso("IKEAPNG.png"),
    width=180
)

st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Menú",
    [
        "Inicio",
        "Carrito Inteligente",
        "Asistente Virtual",
        "Armado Inteligente",
        "Ética y Privacidad",
        "Dashboard IA"
    ]
)



# =====================================================
# HEADER
# =====================================================

if pagina == "Inicio":

    mostrar_inicio()

elif pagina == "Carrito Inteligente":

    mostrar_carrito()

elif pagina == "Asistente Virtual":

    mostrar_chat()

elif pagina == "Ética y Privacidad":

    mostrar_privacidad()

elif pagina == "Dashboard IA":

    mostrar_dashboard()

elif pagina == "Armado Inteligente":

    mostrar_armado()
