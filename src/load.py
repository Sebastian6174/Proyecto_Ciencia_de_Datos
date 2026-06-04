import os
import pandas as pd
from sqlalchemy import create_engine


def load_tables(dfs, output_dir):
    """
    Guarda las tablas del Data Warehouse en CSV
    y también las carga en PostgreSQL.
    """

    # -----------------------------
    # Crear carpeta de salida
    # -----------------------------
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # -----------------------------
    # Conexión PostgreSQL
    # -----------------------------
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/fast_and_safe_dw"
    )

    # -----------------------------
    # Guardar cada tabla
    # -----------------------------
    for name, df in dfs.items():

        # ===== CSV =====
        output_path = os.path.join(output_dir, f"{name}.csv")

        df.to_csv(
            output_path,
            index=False,
            encoding="utf-8"
        )

        print(
            f"Saved {name}.csv ({len(df)} rows) "
            f"to {output_path}"
        )

        # ===== PostgreSQL =====
        df.to_sql(
            name,
            engine,
            if_exists="replace",
            index=False
        )

        print(
            f"Loaded table '{name}' into PostgreSQL "
            f"({len(df)} rows)"
        )

    print("\nLoading phase completed successfully!")