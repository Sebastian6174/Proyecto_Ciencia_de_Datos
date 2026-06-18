import pandas as pd
from sqlalchemy import text
from config import Config
from typing import Dict

def load_tables(dfs: Dict[str, pd.DataFrame], schema: str = "dw", if_exists: str = "replace"):
    """
    Carga las tablas transformadas en Supabase.
    """
    if not dfs:
        raise ValueError("No hay DataFrames para cargar.")

    engine = Config.get_engine()

    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))

        for table_name, df in dfs.items():
            if not isinstance(df, pd.DataFrame):
                raise TypeError(f"La tabla '{table_name}' no es un DataFrame.")

            df.to_sql(
                name=table_name,
                con=connection,
                schema=schema,
                if_exists=if_exists,
                index=False,
                chunksize=1000,
                method="multi",
            )
            print(f"Loaded {schema}.{table_name}: {len(df)} rows")

    print("\nLoading phase completed successfully!")
