import pandas as pd


def build_dim_tipo_novedad(dfs):
    print("Building Dim_Tipo_Novedad...")
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

    unique_novs = nov_merged[["nombre", "descripcion"]].drop_duplicates().reset_index(drop=True)
    unique_novs["Tipo_Novedad_Key"] = unique_novs.index + 1

    default_nov = pd.DataFrame([{
        "nombre": "Sin Novedad",
        "descripcion": "Servicio sin novedades reportadas",
        "Tipo_Novedad_Key": 0
    }])

    dim_tipo_novedad = pd.concat([default_nov, unique_novs], ignore_index=True)
    dim_tipo_novedad = dim_tipo_novedad.rename(columns={
        "nombre": "Categoria_Novedad",
        "descripcion": "Descripcion_Novedad"
    })[["Tipo_Novedad_Key", "Categoria_Novedad", "Descripcion_Novedad"]]

    return dim_tipo_novedad
