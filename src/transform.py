import pandas as pd
import numpy as np

def transform_all(dfs):
    """
    Applies business logic and transformations to operational tables to generate
    dimensions and fact tables.
    """
    # ----------------------------------------------------
    # 1. Dim_Ciudad
    # ----------------------------------------------------
    print("Building Dim_Ciudad...")
    ciudad = dfs["ciudad"].copy()
    dept = dfs["departamento"].copy()
    
    # Standardize column types
    ciudad["ciudad_id"] = pd.to_numeric(ciudad["ciudad_id"])
    ciudad["departamento_id"] = pd.to_numeric(ciudad["departamento_id"])
    dept["departamento_id"] = pd.to_numeric(dept["departamento_id"])
    
    dim_ciudad = pd.merge(ciudad, dept, on="departamento_id", how="left")
    dim_ciudad = dim_ciudad.rename(columns={
        "ciudad_id": "Ciudad_Key",
        "nombre_x": "Nombre_Ciudad",
        "nombre_y": "Departamento"
    })[["Ciudad_Key", "Nombre_Ciudad", "Departamento"]]
    dim_ciudad["Nombre_Ciudad"] = dim_ciudad["Nombre_Ciudad"].str.strip().str.upper()
    dim_ciudad["Departamento"] = dim_ciudad["Departamento"].str.strip().str.upper()
    
    # ----------------------------------------------------
    # 2. Dim_Cliente
    # ----------------------------------------------------
    print("Building Dim_Cliente...")
    cliente = dfs["cliente"].copy()
    cliente["cliente_id"] = pd.to_numeric(cliente["cliente_id"])
    
    dim_cliente = cliente.rename(columns={
        "cliente_id": "Cliente_Key",
        "nit_cliente": "NIT_Cliente",
        "nombre": "Nombre_Empresa",
        "sector": "Sector_Economico"
    })[["Cliente_Key", "NIT_Cliente", "Nombre_Empresa", "Sector_Economico"]]
    dim_cliente["Nombre_Empresa"] = dim_cliente["Nombre_Empresa"].str.strip()
    dim_cliente["Sector_Economico"] = dim_cliente["Sector_Economico"].str.strip()
    
    # ----------------------------------------------------
    # 3. Dim_Sede
    # ----------------------------------------------------
    print("Building Dim_Sede...")
    sede = dfs["sede"].copy()
    sede["sede_id"] = pd.to_numeric(sede["sede_id"])
    
    dim_sede = sede.rename(columns={
        "sede_id": "Sede_Key",
        "nombre": "Nombre_Sede",
        "direccion": "Direccion_Sede"
    })
    # Add Barrio as 'No Especificado'
    dim_sede["Barrio"] = "No Especificado"
    dim_sede = dim_sede[["Sede_Key", "Nombre_Sede", "Direccion_Sede", "Barrio"]]
    
    # ----------------------------------------------------
    # 4. Dim_Mensajero
    # ----------------------------------------------------
    print("Building Dim_Mensajero...")
    mensajero = dfs["clientes_mensajeroaquitoy"].copy()
    user = dfs["auth_user"].copy()
    servicio = dfs["mensajeria_servicio"].copy()
    vehiculo = dfs["mensajeria_tipovehiculo"].copy()
    
    mensajero["id"] = pd.to_numeric(mensajero["id"])
    mensajero["user_id"] = pd.to_numeric(mensajero["user_id"])
    user["id"] = pd.to_numeric(user["id"])
    servicio["mensajero_id"] = pd.to_numeric(servicio["mensajero_id"], errors='coerce')
    vehiculo["id"] = pd.to_numeric(vehiculo["id"])
    
    # Join mensajero and user
    m_user = pd.merge(mensajero, user, left_on="user_id", right_on="id", how="left")
    m_user["Nombre_Completo"] = (m_user["first_name"].fillna("") + " " + m_user["last_name"].fillna("")).str.strip()
    
    # Determine vehicle type from their services
    # Let's count which vehicle each messenger used most frequently
    serv_veh = servicio[["mensajero_id", "tipo_vehiculo_id"]].dropna()
    serv_veh["tipo_vehiculo_id"] = pd.to_numeric(serv_veh["tipo_vehiculo_id"])
    # Join with vehicle name
    serv_veh_name = pd.merge(serv_veh, vehiculo, left_on="tipo_vehiculo_id", right_on="id", how="left")
    
    # Get mode vehicle for each messenger
    def get_mode_veh(group):
        if not group.empty:
            return group["nombre"].mode().iloc[0]
        return "Moto" # Default fallback
    
    mensajero_veh_map = serv_veh_name.groupby("mensajero_id").apply(get_mode_veh)
    if isinstance(mensajero_veh_map, pd.DataFrame):
        # In some pandas versions apply on groupby might return a DF
        mensajero_veh_map = mensajero_veh_map.squeeze()
        
    m_user["Tipo_Vehiculo"] = m_user["id_x"].map(mensajero_veh_map).fillna("Moto")
    
    dim_mensajero = m_user.rename(columns={
        "id_x": "Mensajero_Key",
        "user_id": "ID_Identificacion"
    })[["Mensajero_Key", "ID_Identificacion", "Nombre_Completo", "Tipo_Vehiculo"]]
    
    # Add a default 'No Asignado' record with Key -1
    default_mensajero = pd.DataFrame([{
        "Mensajero_Key": -1,
        "ID_Identificacion": 0,
        "Nombre_Completo": "No Asignado",
        "Tipo_Vehiculo": "No Especificado"
    }])
    dim_mensajero = pd.concat([default_mensajero, dim_mensajero], ignore_index=True)
    
    # ----------------------------------------------------
    # 5. Dim_Tipo_Urgencia
    # ----------------------------------------------------
    print("Building Dim_Tipo_Urgencia...")
    # Define based on values found in db:
    # 'Alta: En una hora', 'Media: De 1 - 3 Horas', 'Baja: Transcurso del Dia'
    urgencia_data = [
        {"Tipo_Urgencia_Key": 1, "Categoria_Urgencia": "Alta", "Tiempo_Promesa_Horas": 1},
        {"Tipo_Urgencia_Key": 2, "Categoria_Urgencia": "Media", "Tiempo_Promesa_Horas": 3},
        {"Tipo_Urgencia_Key": 3, "Categoria_Urgencia": "Baja", "Tiempo_Promesa_Horas": 12},
        {"Tipo_Urgencia_Key": -1, "Categoria_Urgencia": "No Especificada", "Tiempo_Promesa_Horas": 0}
    ]
    dim_tipo_urgencia = pd.DataFrame(urgencia_data)
    
    # Map priority text from DB to Key
    def get_urgency_key(prio_str):
        if pd.isna(prio_str):
            return -1
        prio_str_lower = str(prio_str).lower()
        if "alta" in prio_str_lower or "una hora" in prio_str_lower:
            return 1
        elif "media" in prio_str_lower or "1 a 3" in prio_str_lower or "1 - 3" in prio_str_lower:
            return 2
        elif "baja" in prio_str_lower or "transcurso" in prio_str_lower:
            return 3
        return -1
        
    # ----------------------------------------------------
    # 6. Dim_Servicio
    # ----------------------------------------------------
    print("Building Dim_Servicio...")
    # Formed from mensajeria_servicio
    dim_servicio = servicio[["id", "fecha_solicitud", "descripcion"]].copy()
    dim_servicio["id"] = pd.to_numeric(dim_servicio["id"])
    dim_servicio["fecha_solicitud"] = pd.to_datetime(dim_servicio["fecha_solicitud"])
    
    dim_servicio["Servicio_Key"] = dim_servicio["id"]
    dim_servicio["Codigo_Guia"] = dim_servicio.apply(
        lambda r: f"SRV-{r['fecha_solicitud'].year}-{r['id']}" if pd.notna(r['fecha_solicitud']) else f"SRV-2024-{r['id']}",
        axis=1
    )
    dim_servicio = dim_servicio.rename(columns={
        "descripcion": "Instrucciones_Especiales"
    })[["Servicio_Key", "Codigo_Guia", "Instrucciones_Especiales"]]
    dim_servicio["Instrucciones_Especiales"] = dim_servicio["Instrucciones_Especiales"].str.strip().fillna("Sin instrucciones")
    
    # ----------------------------------------------------
    # 7. Dim_Tipo_Novedad
    # ----------------------------------------------------
    print("Building Dim_Tipo_Novedad...")
    nov_serv = dfs["mensajeria_novedadesservicio"].copy()
    nov_tipo = dfs["mensajeria_tiponovedad"].copy()
    
    nov_serv["tipo_novedad_id"] = pd.to_numeric(nov_serv["tipo_novedad_id"])
    nov_tipo["id"] = pd.to_numeric(nov_tipo["id"])
    
    # Merge to get Categoria_Novedad
    nov_merged = pd.merge(nov_serv, nov_tipo, left_on="tipo_novedad_id", right_on="id", how="left")
    nov_merged["descripcion"] = nov_merged["descripcion"].str.strip().fillna("Sin descripción").replace("", "Sin descripción")
    nov_merged["nombre"] = nov_merged["nombre"].str.strip().fillna("General")
    
    # Find unique combinations of Category and Description
    unique_novs = nov_merged[["nombre", "descripcion"]].drop_duplicates().reset_index(drop=True)
    unique_novs["Tipo_Novedad_Key"] = unique_novs.index + 1
    
    # Add a default 'Sin Novedad' record
    default_nov = pd.DataFrame([{"nombre": "Sin Novedad", "descripcion": "Servicio sin novedades reportadas", "Tipo_Novedad_Key": 0}])
    dim_tipo_novedad = pd.concat([default_nov, unique_novs], ignore_index=True)
    dim_tipo_novedad = dim_tipo_novedad.rename(columns={
        "nombre": "Categoria_Novedad",
        "descripcion": "Descripcion_Novedad"
    })[["Tipo_Novedad_Key", "Categoria_Novedad", "Descripcion_Novedad"]]
    
    # Map (tipo_novedad_id, descripcion) to Tipo_Novedad_Key for Fact table
    # Standardize names for joining
    nov_merged_key = pd.merge(
        nov_merged, 
        dim_tipo_novedad.rename(columns={"Categoria_Novedad": "nombre", "Descripcion_Novedad": "descripcion"}), 
        on=["nombre", "descripcion"], 
        how="left"
    )
    
    # ----------------------------------------------------
    # 8. Dim_Hora
    # ----------------------------------------------------
    print("Building Dim_Hora...")
    horas = []
    for h in range(24):
        if 0 <= h <= 5:
            franja = "Madrugada"
        elif 6 <= h <= 11:
            franja = "Mañana"
        elif 12 <= h <= 17:
            franja = "Tarde"
        else:
            franja = "Noche"
        horas.append({
            "Hora_Key": h,
            "Hora_Militar": f"{h:02d}",
            "Franja_Horaria": franja
        })
    dim_hora = pd.DataFrame(horas)
    # Add a default 'Hora No Especificada' record with Key -1
    default_hora = pd.DataFrame([{
        "Hora_Key": -1,
        "Hora_Militar": "N/A",
        "Franja_Horaria": "No Especificada"
    }])
    dim_hora = pd.concat([default_hora, dim_hora], ignore_index=True)
    
    # ----------------------------------------------------
    # 9. Dim_Fecha
    # ----------------------------------------------------
    print("Building Dim_Fecha...")
    # Gather all dates from services and updates
    all_dates = set()
    
    # Service dates
    for col in ["fecha_solicitud", "fecha_deseada"]:
        valid_dates = pd.to_datetime(dfs["mensajeria_servicio"][col], errors='coerce').dropna()
        all_dates.update(valid_dates.dt.date)
        
    # State update dates
    valid_dates = pd.to_datetime(dfs["mensajeria_estadosservicio"]["fecha"], errors='coerce').dropna()
    all_dates.update(valid_dates.dt.date)
    
    # Novelty dates
    valid_dates = pd.to_datetime(dfs["mensajeria_novedadesservicio"]["fecha_novedad"], errors='coerce').dropna()
    all_dates.update(valid_dates.dt.date)
    
    # Filter out outlier dates (e.g. year 0004 or 9024) to keep date range reasonable
    all_dates = {d for d in all_dates if d is not None and 2020 <= d.year <= 2026}
    
    if all_dates:
        min_date = min(all_dates)
        max_date = max(all_dates)
    else:
        # Fallbacks
        min_date = pd.to_datetime("2023-01-01").date()
        max_date = pd.to_datetime("2024-12-31").date()
        
    date_range = pd.date_range(min_date, max_date)
    
    spanish_days = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    spanish_months = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    
    fechas = []
    for dt in date_range:
        fechas.append({
            "Fecha_Key": int(dt.strftime("%Y%m%d")),
            "Fecha_Completa": dt.strftime("%d/%m/%Y"),
            "Dia_Semana": spanish_days[int(dt.strftime("%w"))], # %w is 0=Sunday, 6=Saturday
            "Mes": spanish_months[dt.month],
            "Anio": dt.year
        })
    dim_fecha = pd.DataFrame(fechas)
    
    # Add a default 'Fecha No Especificada' row
    default_fecha = pd.DataFrame([{
        "Fecha_Key": -1,
        "Fecha_Completa": "00/00/0000",
        "Dia_Semana": "No Especificado",
        "Mes": "No Especificado",
        "Anio": 0
    }])
    dim_fecha = pd.concat([default_fecha, dim_fecha], ignore_index=True)

    # Helper helper to convert dates to YYYYMMDD
    def to_date_key(dt_series):
        dt_conv = pd.to_datetime(dt_series, errors='coerce')
        return dt_conv.apply(lambda x: int(x.strftime("%Y%m%d")) if pd.notna(x) else -1)

    # ----------------------------------------------------
    # 10. Fact_Servicios
    # ----------------------------------------------------
    print("Building Fact_Servicios...")
    # Cycle of status times for each service
    estados = dfs["mensajeria_estadosservicio"].copy()
    estados["servicio_id"] = pd.to_numeric(estados["servicio_id"])
    estados["estado_id"] = pd.to_numeric(estados["estado_id"])
    estados["timestamp"] = pd.to_datetime(estados["fecha"].astype(str) + " " + estados["hora"].astype(str), errors='coerce')
    
    # Get first occurrence of each status for each service
    states_grouped = estados.groupby(["servicio_id", "estado_id"])["timestamp"].min().unstack()
    
    # Join state timestamps with services
    serv = dfs["mensajeria_servicio"].copy()
    serv["id"] = pd.to_numeric(serv["id"])
    serv["solicitud_timestamp"] = pd.to_datetime(serv["fecha_solicitud"].astype(str) + " " + serv["hora_solicitud"].astype(str), errors='coerce')
    
    # Join states
    # Columns in states_grouped correspond to status IDs: 1 (Iniciado), 2 (Asignado), 4 (Recogido), 5 (Entregado), 6 (Terminado)
    serv = serv.join(states_grouped, on="id")
    
    # Rename state columns for readability
    serv = serv.rename(columns={
        1: "ts_iniciado",
        2: "ts_asignado",
        4: "ts_recogido",
        5: "ts_entregado",
        6: "ts_cierre"
    })
    
    # If state 1 timestamp is missing, use solicitud_timestamp
    serv["ts_iniciado"] = serv["ts_iniciado"].fillna(serv["solicitud_timestamp"])
    
    # Calculate duration metrics in minutes
    # Total Delivery Time: Solicitud to Cierre (or Entrega if Cierre is missing)
    cierre_or_entrega = serv["ts_cierre"].fillna(serv["ts_entregado"])
    serv["Tiempo_Total_Entrega"] = (cierre_or_entrega - serv["solicitud_timestamp"]).dt.total_seconds() / 60.0
    
    # Assignment Time: Iniciado/Solicitud to Asignado
    serv["Tiempo_Asignacion"] = (serv["ts_asignado"] - serv["ts_iniciado"]).dt.total_seconds() / 60.0
    
    # Pickup Time: Asignado to Recogido
    serv["Tiempo_Recogida"] = (serv["ts_recogido"] - serv["ts_asignado"]).dt.total_seconds() / 60.0
    
    # Delivery Time: Recogido to Entrega
    serv["Tiempo_Entrega"] = (serv["ts_entregado"] - serv["ts_recogido"]).dt.total_seconds() / 60.0
    
    # Replace negative or infinite values with NaN
    for col in ["Tiempo_Total_Entrega", "Tiempo_Asignacion", "Tiempo_Recogida", "Tiempo_Entrega"]:
        serv.loc[serv[col] < 0, col] = np.nan
        serv[col] = serv[col].round(1)
        
    # Get Sede Key via usuario_id
    users_aq = dfs["clientes_usuarioaquitoy"].copy()
    users_aq["id"] = pd.to_numeric(users_aq["id"])
    users_aq["sede_id"] = pd.to_numeric(users_aq["sede_id"])
    
    serv["usuario_id"] = pd.to_numeric(serv["usuario_id"])
    serv = pd.merge(serv, users_aq[["id", "sede_id"]], left_on="usuario_id", right_on="id", how="left", suffixes=("", "_user"))
    
    # Set Sede_Key (default to -1 if missing)
    serv["Sede_Key"] = serv["sede_id"].fillna(-1).astype(int)
    
    # Keys
    serv["Fecha_Solicitud_Key"] = to_date_key(serv["fecha_solicitud"])
    serv["Fecha_Asignacion_Key"] = to_date_key(serv["ts_asignado"].dt.date)
    serv["Fecha_Cierre_Key"] = to_date_key(cierre_or_entrega.dt.date)
    
    serv["Hora_Solicitud_Key"] = serv["solicitud_timestamp"].dt.hour.fillna(-1).astype(int)
    serv["Hora_Asignacion_Key"] = serv["ts_asignado"].dt.hour.fillna(-1).astype(int)
    serv["Hora_Cierre_Key"] = cierre_or_entrega.dt.hour.fillna(-1).astype(int)
    
    serv["Mensajero_Key"] = pd.to_numeric(serv["mensajero_id"]).fillna(-1).astype(int)
    serv["Cliente_Key"] = pd.to_numeric(serv["cliente_id"]).fillna(-1).astype(int)
    serv["Ciudad_Origen_Key"] = pd.to_numeric(serv["ciudad_origen_id"]).fillna(-1).astype(int)
    serv["Ciudad_Destino_Key"] = pd.to_numeric(serv["ciudad_destino_id"]).fillna(-1).astype(int)
    
    serv["Tipo_Urgencia_Key"] = serv["prioridad"].apply(get_urgency_key)
    serv["Servicio_Key"] = serv["id"]
    serv["Cantidad_Servicios"] = 1
    
    fact_servicios = serv[[
        "Fecha_Solicitud_Key", "Fecha_Asignacion_Key", "Fecha_Cierre_Key",
        "Hora_Solicitud_Key", "Hora_Asignacion_Key", "Hora_Cierre_Key",
        "Mensajero_Key", "Cliente_Key", "Sede_Key",
        "Ciudad_Origen_Key", "Ciudad_Destino_Key", "Tipo_Urgencia_Key", "Servicio_Key",
        "Tiempo_Total_Entrega", "Tiempo_Asignacion", "Tiempo_Recogida", "Tiempo_Entrega",
        "Cantidad_Servicios"
    ]]
    
    # ----------------------------------------------------
    # 11. Fact_Novedades
    # ----------------------------------------------------
    print("Building Fact_Novedades...")
    # Map nov_merged_key to the fact table columns
    # Columns in fact: FK: Fecha_Key, FK: Mensajero_Key, FK: Tipo_Novedad_Key, FK: Servicio_Key, Cantidad_Novedades
    nov_merged_key["Fecha_Key"] = to_date_key(nov_merged_key["fecha_novedad"])
    nov_merged_key["Mensajero_Key"] = pd.to_numeric(nov_merged_key["mensajero_id"]).fillna(-1).astype(int)
    nov_merged_key["Tipo_Novedad_Key"] = pd.to_numeric(nov_merged_key["Tipo_Novedad_Key"]).fillna(0).astype(int)
    nov_merged_key["Servicio_Key"] = pd.to_numeric(nov_merged_key["servicio_id"]).fillna(-1).astype(int)
    nov_merged_key["Cantidad_Novedades"] = 1
    
    fact_novedades = nov_merged_key[[
        "Fecha_Key", "Mensajero_Key", "Tipo_Novedad_Key", "Servicio_Key", "Cantidad_Novedades"
    ]]
    
    return {
        "Dim_Ciudad": dim_ciudad,
        "Dim_Cliente": dim_cliente,
        "Dim_Sede": dim_sede,
        "Dim_Mensajero": dim_mensajero,
        "Dim_Tipo_Urgencia": dim_tipo_urgencia,
        "Dim_Servicio": dim_servicio,
        "Dim_Tipo_Novedad": dim_tipo_novedad,
        "Dim_Hora": dim_hora,
        "Dim_Fecha": dim_fecha,
        "Fact_Servicios": fact_servicios,
        "Fact_Novedades": fact_novedades
    }
