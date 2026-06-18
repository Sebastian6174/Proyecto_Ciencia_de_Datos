import pandas as pd


def build_dim_ciudad(dfs):
    print("Building Dim_Ciudad...")
    ciudad = dfs["ciudad"].copy()
    dept = dfs["departamento"].copy()

    ciudad["ciudad_id"] = pd.to_numeric(ciudad["ciudad_id"])
    ciudad["departamento_id"] = pd.to_numeric(ciudad["departamento_id"])
    dept["departamento_id"] = pd.to_numeric(dept["departamento_id"])

    dim_ciudad = pd.merge(ciudad, dept, on="departamento_id", how="left")
    dim_ciudad = dim_ciudad.rename(columns={
        "ciudad_id": "Ciudad_Key",
        "nombre_x": "Nombre_Ciudad",
        "nombre_y": "Departamento"
    })[["Ciudad_Key", "Nombre_Ciudad", "Departamento"]]

    dim_ciudad["Nombre_Ciudad"] = dim_ciudad["Nombre_Ciudad"].astype(str).str.strip().str.upper()
    dim_ciudad["Departamento"] = dim_ciudad["Departamento"].astype(str).str.strip().str.upper()

    return dim_ciudad
