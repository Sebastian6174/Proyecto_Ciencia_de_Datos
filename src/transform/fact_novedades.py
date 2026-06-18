import pandas as pd


def build_fact_novedades(dfs, dim_tipo_novedad, dim_mensajero, dim_servicio):
    print("Building Fact_Novedades...")
    nov_serv = dfs["mensajeria_novedadesservicio"].copy()
    nov_tipo = dfs["mensajeria_tiponovedad"].copy()

    nov_serv["tipo_novedad_id"] = pd.to_numeric(nov_serv["tipo_novedad_id"], errors="coerce")
    nov_tipo["id"] = pd.to_numeric(nov_tipo["id"], errors="coerce")

    nov_merged = pd.merge(
        nov_serv,
        nov_tipo,
        left_on="tipo_novedad_id",
        right_on="id",
        how="left"
    )

    nov_merged["descripcion"] = nov_merged["descripcion"].astype(str).str.strip().replace({"nan": "Sin descripción", "": "Sin descripción"})
    nov_merged["nombre"] = nov_merged["nombre"].astype(str).str.strip().replace({"nan": "General", "": "General"})

    nov_merged_key = pd.merge(
        nov_merged,
        dim_tipo_novedad.rename(columns={"Categoria_Novedad": "nombre", "Descripcion_Novedad": "descripcion"}),
        on=["nombre", "descripcion"],
        how="left"
    )

    nov_merged_key["Fecha_Key"] = pd.to_datetime(nov_merged_key["fecha_novedad"], errors="coerce").apply(
        lambda x: int(x.strftime("%Y%m%d")) if pd.notna(x) else -1
    )

    nov_merged_key["mensajero_id"] = pd.to_numeric(nov_merged_key["mensajero_id"], errors="coerce")
    nov_merged_key["servicio_id"] = pd.to_numeric(nov_merged_key["servicio_id"], errors="coerce")
    mensajero_key_map = dim_mensajero.dropna(subset=["Mensajero_Source_Id"]).set_index("Mensajero_Source_Id")["Mensajero_Key"]
    servicio_key_map = dim_servicio.set_index("Servicio_Source_Id")["Servicio_Key"]

    nov_merged_key["Mensajero_Key"] = nov_merged_key["mensajero_id"].map(mensajero_key_map).fillna(-1).astype(int)
    nov_merged_key["Tipo_Novedad_Key"] = pd.to_numeric(nov_merged_key["Tipo_Novedad_Key"], errors="coerce").fillna(0).astype(int)
    nov_merged_key["Servicio_Key"] = nov_merged_key["servicio_id"].map(servicio_key_map).fillna(-1).astype(int)
    nov_merged_key["Cantidad_Novedades"] = 1

    return nov_merged_key[[
        "Fecha_Key", "Mensajero_Key", "Tipo_Novedad_Key", "Servicio_Key", "Cantidad_Novedades"
    ]]
