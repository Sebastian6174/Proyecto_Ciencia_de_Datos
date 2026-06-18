import pandas as pd


def build_dim_cliente(dfs):
    print("Building Dim_Cliente...")
    cliente = dfs["cliente"].copy()
    cliente["cliente_id"] = pd.to_numeric(cliente["cliente_id"], errors="coerce")

    dim_cliente = cliente.rename(columns={
        "cliente_id": "Cliente_Source_Id",
        "nit_cliente": "NIT_Cliente",
        "nombre": "Nombre_Empresa",
        "sector": "Sector_Economico"
    })[["Cliente_Source_Id", "NIT_Cliente", "Nombre_Empresa", "Sector_Economico"]]

    dim_cliente["Nombre_Empresa"] = dim_cliente["Nombre_Empresa"].astype(str).str.strip()
    dim_cliente["Sector_Economico"] = dim_cliente["Sector_Economico"].astype(str).str.strip()
    dim_cliente = dim_cliente.drop_duplicates(subset=["Cliente_Source_Id"]).reset_index(drop=True)
    dim_cliente.insert(0, "Cliente_Key", range(1, len(dim_cliente) + 1))

    default_cliente = pd.DataFrame([{
        "Cliente_Key": -1,
        "Cliente_Source_Id": pd.NA,
        "NIT_Cliente": "N/A",
        "Nombre_Empresa": "No Especificada",
        "Sector_Economico": "No Especificado"
    }])

    return pd.concat([default_cliente, dim_cliente], ignore_index=True)
