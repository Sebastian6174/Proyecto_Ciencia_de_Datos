import pandas as pd


def build_dim_ciudad(dfs):
    print("Building Dim_Ciudad...")
    ciudad = dfs["ciudad"].copy()
    dept = dfs["departamento"].copy()

    ciudad["ciudad_id"] = pd.to_numeric(ciudad["ciudad_id"], errors="coerce")
    ciudad["departamento_id"] = pd.to_numeric(ciudad["departamento_id"], errors="coerce")
    dept["departamento_id"] = pd.to_numeric(dept["departamento_id"], errors="coerce")

    dim_ciudad = pd.merge(ciudad, dept, on="departamento_id", how="left")
    dim_ciudad = dim_ciudad.rename(columns={
        "ciudad_id": "Ciudad_Source_Id",
        "nombre_x": "Nombre_Ciudad",
        "nombre_y": "Departamento"
    })[["Ciudad_Source_Id", "Nombre_Ciudad", "Departamento"]]

    dim_ciudad["Nombre_Ciudad"] = dim_ciudad["Nombre_Ciudad"].astype(str).str.strip().str.upper()
    dim_ciudad["Departamento"] = dim_ciudad["Departamento"].astype(str).str.strip().str.upper()
    dim_ciudad = dim_ciudad.drop_duplicates(subset=["Ciudad_Source_Id"]).reset_index(drop=True)
    dim_ciudad.insert(0, "Ciudad_Key", range(1, len(dim_ciudad) + 1))

    default_ciudad = pd.DataFrame([{
        "Ciudad_Key": -1,
        "Ciudad_Source_Id": pd.NA,
        "Nombre_Ciudad": "NO ESPECIFICADA",
        "Departamento": "NO ESPECIFICADO"
    }])

    return pd.concat([default_ciudad, dim_ciudad], ignore_index=True)
