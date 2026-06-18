import pandas as pd


def build_dim_sede(dfs):
    print("Building Dim_Sede...")
    sede = dfs["sede"].copy()
    sede["sede_id"] = pd.to_numeric(sede["sede_id"])

    dim_sede = sede.rename(columns={
        "sede_id": "Sede_Key",
        "nombre": "Nombre_Sede",
        "direccion": "Direccion_Sede"
    })
    dim_sede["Barrio"] = "No Especificado"
    dim_sede = dim_sede[["Sede_Key", "Nombre_Sede", "Direccion_Sede", "Barrio"]]

    return dim_sede
