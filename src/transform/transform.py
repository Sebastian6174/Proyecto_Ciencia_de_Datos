import pandas as pd
from typing import Dict
from transform import (
    build_dim_ciudad,
    build_dim_cliente,
    build_dim_sede,
    build_dim_mensajero,
    build_dim_tipo_urgencia,
    get_urgency_key,
    build_dim_servicio,
    build_dim_tipo_novedad,
    build_dim_hora,
    build_dim_fecha,
    build_fact_servicios,
    build_fact_novedades,
)

def transform_all(dfs : Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Applies business logic and transformations to operational tables to generate
    dimensions and fact tables.
    """
    dim_ciudad = build_dim_ciudad(dfs)
    dim_cliente = build_dim_cliente(dfs)
    dim_sede = build_dim_sede(dfs)
    dim_mensajero = build_dim_mensajero(dfs)
    dim_tipo_urgencia = build_dim_tipo_urgencia()
    dim_servicio = build_dim_servicio(dfs)
    dim_tipo_novedad = build_dim_tipo_novedad(dfs)
    dim_hora = build_dim_hora()
    dim_fecha = build_dim_fecha(dfs)

    fact_servicios = build_fact_servicios(
        dfs,
        get_urgency_key,
        dim_ciudad,
        dim_cliente,
        dim_sede,
        dim_mensajero,
        dim_servicio,
    )
    fact_novedades = build_fact_novedades(dfs, dim_tipo_novedad, dim_mensajero, dim_servicio)

    return {
        "dim_ciudad": dim_ciudad,
        "dim_cliente": dim_cliente,
        "dim_sede": dim_sede,
        "dim_mensajero": dim_mensajero,
        "dim_tipo_urgencia": dim_tipo_urgencia,
        "dim_servicio": dim_servicio,
        "dim_tipo_novedad": dim_tipo_novedad,
        "dim_hora": dim_hora,
        "dim_fecha": dim_fecha,
        "fact_servicios": fact_servicios,
        "fact_novedades": fact_novedades,
    }
