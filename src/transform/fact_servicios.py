import pandas as pd


def to_date_key(dt_series):
    dt_conv = pd.to_datetime(dt_series, errors="coerce")
    return dt_conv.apply(lambda x: int(x.strftime("%Y%m%d")) if pd.notna(x) else -1)


def build_fact_servicios(
    dfs,
    get_urgency_key,
    dim_ciudad,
    dim_cliente,
    dim_sede,
    dim_mensajero,
    dim_servicio,
):
    print("Building Fact_Servicios...")
    estados = dfs["mensajeria_estadosservicio"].copy()
    estados["servicio_id"] = pd.to_numeric(estados["servicio_id"], errors="coerce")
    estados["estado_id"] = pd.to_numeric(estados["estado_id"], errors="coerce")
    estados["timestamp"] = pd.to_datetime(
        estados["fecha"].astype(str) + " " + estados["hora"].astype(str),
        errors="coerce"
    )

    states_grouped = estados.groupby(["servicio_id", "estado_id"])["timestamp"].min().unstack()

    serv = dfs["mensajeria_servicio"].copy()
    serv["id"] = pd.to_numeric(serv["id"], errors="coerce")
    serv["solicitud_timestamp"] = pd.to_datetime(
        serv["fecha_solicitud"].astype(str) + " " + serv["hora_solicitud"].astype(str),
        errors="coerce"
    )
    serv = serv.join(states_grouped, on="id")

    serv = serv.rename(columns={
        1: "ts_iniciado",
        2: "ts_asignado",
        4: "ts_recogido",
        5: "ts_entregado",
        6: "ts_cierre"
    })

    serv["ts_iniciado"] = serv["ts_iniciado"].fillna(serv["solicitud_timestamp"])
    cierre_or_entrega = serv["ts_cierre"].fillna(serv["ts_entregado"])

    serv["Tiempo_Total_Entrega"] = (cierre_or_entrega - serv["solicitud_timestamp"]).dt.total_seconds() / 60.0
    serv["Tiempo_Asignacion"] = (serv["ts_asignado"] - serv["ts_iniciado"]).dt.total_seconds() / 60.0
    serv["Tiempo_Recogida"] = (serv["ts_recogido"] - serv["ts_asignado"]).dt.total_seconds() / 60.0
    serv["Tiempo_Entrega"] = (serv["ts_entregado"] - serv["ts_recogido"]).dt.total_seconds() / 60.0

    for col in ["Tiempo_Total_Entrega", "Tiempo_Asignacion", "Tiempo_Recogida", "Tiempo_Entrega"]:
        serv.loc[serv[col] < 0, col] = pd.NA
        serv[col] = serv[col].round(1)

    users_aq = dfs["clientes_usuarioaquitoy"].copy()
    users_aq["id"] = pd.to_numeric(users_aq["id"], errors="coerce")
    users_aq["sede_id"] = pd.to_numeric(users_aq["sede_id"], errors="coerce")

    serv["usuario_id"] = pd.to_numeric(serv["usuario_id"], errors="coerce")
    serv = pd.merge(
        serv,
        users_aq[["id", "sede_id"]],
        left_on="usuario_id",
        right_on="id",
        how="left",
        suffixes=("", "_user")
    )

    ciudad_key_map = dim_ciudad.set_index("Ciudad_Source_Id")["Ciudad_Key"]
    cliente_key_map = dim_cliente.set_index("Cliente_Source_Id")["Cliente_Key"]
    sede_key_map = dim_sede.set_index("Sede_Source_Id")["Sede_Key"]
    mensajero_key_map = dim_mensajero.dropna(subset=["Mensajero_Source_Id"]).set_index("Mensajero_Source_Id")["Mensajero_Key"]
    servicio_key_map = dim_servicio.set_index("Servicio_Source_Id")["Servicio_Key"]

    serv["Sede_Key"] = serv["sede_id"].map(sede_key_map).fillna(-1).astype(int)
    serv["Fecha_Solicitud_Key"] = to_date_key(serv["fecha_solicitud"])
    serv["Fecha_Asignacion_Key"] = to_date_key(serv["ts_asignado"].dt.date)
    serv["Fecha_Cierre_Key"] = to_date_key(cierre_or_entrega.dt.date)

    serv["Hora_Solicitud_Key"] = serv["solicitud_timestamp"].dt.hour.fillna(-1).astype(int)
    serv["Hora_Asignacion_Key"] = serv["ts_asignado"].dt.hour.fillna(-1).astype(int)
    serv["Hora_Cierre_Key"] = cierre_or_entrega.dt.hour.fillna(-1).astype(int)

    for col in ["mensajero_id", "cliente_id", "ciudad_origen_id", "ciudad_destino_id", "id"]:
        serv[col] = pd.to_numeric(serv[col], errors="coerce")

    serv["Mensajero_Key"] = serv["mensajero_id"].map(mensajero_key_map).fillna(-1).astype(int)
    serv["Cliente_Key"] = serv["cliente_id"].map(cliente_key_map).fillna(-1).astype(int)
    serv["Ciudad_Origen_Key"] = serv["ciudad_origen_id"].map(ciudad_key_map).fillna(-1).astype(int)
    serv["Ciudad_Destino_Key"] = serv["ciudad_destino_id"].map(ciudad_key_map).fillna(-1).astype(int)

    serv["Tipo_Urgencia_Key"] = serv["prioridad"].apply(get_urgency_key)
    serv["Servicio_Key"] = serv["id"].map(servicio_key_map).fillna(-1).astype(int)
    serv["Cantidad_Servicios"] = 1

    return serv[[
        "Fecha_Solicitud_Key", "Fecha_Asignacion_Key", "Fecha_Cierre_Key",
        "Hora_Solicitud_Key", "Hora_Asignacion_Key", "Hora_Cierre_Key",
        "Mensajero_Key", "Cliente_Key", "Sede_Key",
        "Ciudad_Origen_Key", "Ciudad_Destino_Key", "Tipo_Urgencia_Key", "Servicio_Key",
        "Tiempo_Total_Entrega", "Tiempo_Asignacion", "Tiempo_Recogida", "Tiempo_Entrega",
        "Cantidad_Servicios"
    ]]
