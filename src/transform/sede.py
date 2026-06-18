import pandas as pd


def build_dim_sede(dfs):
    print("Building Dim_Sede...")
    sede = dfs["sede"].copy()
    sede["sede_id"] = pd.to_numeric(sede["sede_id"], errors="coerce")

    dim_sede = sede.rename(columns={
        "sede_id": "Sede_Source_Id",
        "nombre": "Nombre_Sede",
        "direccion": "Direccion_Sede"
    })
    dim_sede["Barrio"] = "No Especificado"
    dim_sede = dim_sede[["Sede_Source_Id", "Nombre_Sede", "Direccion_Sede", "Barrio"]]
    dim_sede = dim_sede.drop_duplicates(subset=["Sede_Source_Id"]).reset_index(drop=True)
    dim_sede.insert(0, "Sede_Key", range(1, len(dim_sede) + 1))

    default_sede = pd.DataFrame([{
        "Sede_Key": -1,
        "Sede_Source_Id": pd.NA,
        "Nombre_Sede": "No Especificada",
        "Direccion_Sede": "No Especificada",
        "Barrio": "No Especificado"
    }])

    return pd.concat([default_sede, dim_sede], ignore_index=True)
