"""Reglas de la simulación de riesgo, independientes de la interfaz."""


def ajustar_riesgo(probabilidad, tiempo_carrito, productos_vistos, visitas_recientes):
    riesgo = probabilidad * 100
    if tiempo_carrito > 20:
        riesgo += 10
    if productos_vistos > 15:
        riesgo -= 5
    if visitas_recientes > 8:
        riesgo -= 5
    return max(0.0, min(riesgo, 100.0))
