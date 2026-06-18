import pandas as pd


def build_dim_servicio(dfs):
    print("Building Dim_Servicio...")
    servicio = dfs["mensajeria_servicio"].copy()
    dim_servicio = servicio[["id", "fecha_solicitud", "descripcion"]].copy()
    dim_servicio["id"] = pd.to_numeric(dim_servicio["id"])
    dim_servicio["fecha_solicitud"] = pd.to_datetime(dim_servicio["fecha_solicitud"], errors="coerce")

    dim_servicio["Servicio_Key"] = dim_servicio["id"]
    dim_servicio["Codigo_Guia"] = dim_servicio.apply(
        lambda r: f"SRV-{r['fecha_solicitud'].year}-{r['id']}" if pd.notna(r['fecha_solicitud']) else f"SRV-2024-{r['id']}",
        axis=1
    )
    dim_servicio = dim_servicio.rename(columns={
        "descripcion": "Instrucciones_Especiales"
    })[["Servicio_Key", "Codigo_Guia", "Instrucciones_Especiales"]]
    dim_servicio["Instrucciones_Especiales"] = dim_servicio["Instrucciones_Especiales"].astype(str).str.strip().replace({"nan": "Sin instrucciones"})
    dim_servicio["Instrucciones_Especiales"] = dim_servicio["Instrucciones_Especiales"].replace("None", "Sin instrucciones")
    dim_servicio["Instrucciones_Especiales"] = dim_servicio["Instrucciones_Especiales"].fillna("Sin instrucciones")

    return dim_servicio
