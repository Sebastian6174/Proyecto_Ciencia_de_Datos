import pandas as pd


def build_dim_mensajero(dfs):
    print("Building Dim_Mensajero...")
    mensajero = dfs["clientes_mensajeroaquitoy"].copy()
    user = dfs["auth_user"].copy()
    servicio = dfs["mensajeria_servicio"].copy()
    vehiculo = dfs["mensajeria_tipovehiculo"].copy()

    mensajero["id"] = pd.to_numeric(mensajero["id"], errors="coerce")
    mensajero["user_id"] = pd.to_numeric(mensajero["user_id"], errors="coerce")
    user["id"] = pd.to_numeric(user["id"], errors="coerce")
    servicio["mensajero_id"] = pd.to_numeric(servicio["mensajero_id"], errors="coerce")
    vehiculo["id"] = pd.to_numeric(vehiculo["id"], errors="coerce")

    m_user = pd.merge(mensajero, user, left_on="user_id", right_on="id", how="left")
    m_user["Nombre_Completo"] = (
        m_user["first_name"].fillna("") + " " + m_user["last_name"].fillna("")
    ).str.strip()

    serv_veh = servicio[["mensajero_id", "tipo_vehiculo_id"]].dropna()
    serv_veh["tipo_vehiculo_id"] = pd.to_numeric(serv_veh["tipo_vehiculo_id"])
    serv_veh_name = pd.merge(
        serv_veh,
        vehiculo,
        left_on="tipo_vehiculo_id",
        right_on="id",
        how="left"
    )

    def get_mode_veh(group):
        if not group.empty:
            return group["nombre"].mode().iloc[0]
        return "Moto"

    mensajero_veh_map = serv_veh_name.groupby("mensajero_id").apply(get_mode_veh)
    if isinstance(mensajero_veh_map, pd.DataFrame):
        mensajero_veh_map = mensajero_veh_map.squeeze()

    m_user["Tipo_Vehiculo"] = m_user["id_x"].map(mensajero_veh_map).fillna("Moto")

    dim_mensajero = m_user.rename(columns={
        "id_x": "Mensajero_Source_Id",
        "user_id": "ID_Identificacion"
    })[["Mensajero_Source_Id", "ID_Identificacion", "Nombre_Completo", "Tipo_Vehiculo"]]

    dim_mensajero = dim_mensajero.drop_duplicates(subset=["Mensajero_Source_Id"]).reset_index(drop=True)
    dim_mensajero.insert(0, "Mensajero_Key", range(1, len(dim_mensajero) + 1))

    default_mensajero = pd.DataFrame([{
        "Mensajero_Key": -1,
        "Mensajero_Source_Id": pd.NA,
        "ID_Identificacion": 0,
        "Nombre_Completo": "No Asignado",
        "Tipo_Vehiculo": "No Especificado"
    }])

    dim_mensajero = pd.concat([default_mensajero, dim_mensajero], ignore_index=True)

    return dim_mensajero
