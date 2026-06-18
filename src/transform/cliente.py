import pandas as pd


def build_dim_cliente(dfs):
    print("Building Dim_Cliente...")
    cliente = dfs["cliente"].copy()
    cliente["cliente_id"] = pd.to_numeric(cliente["cliente_id"])

    dim_cliente = cliente.rename(columns={
        "cliente_id": "Cliente_Key",
        "nit_cliente": "NIT_Cliente",
        "nombre": "Nombre_Empresa",
        "sector": "Sector_Economico"
    })[["Cliente_Key", "NIT_Cliente", "Nombre_Empresa", "Sector_Economico"]]

    dim_cliente["Nombre_Empresa"] = dim_cliente["Nombre_Empresa"].astype(str).str.strip()
    dim_cliente["Sector_Economico"] = dim_cliente["Sector_Economico"].astype(str).str.strip()

    return dim_cliente
