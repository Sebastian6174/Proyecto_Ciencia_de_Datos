import os
import sys
import time

# Ensure src/ is in the python search path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from extract import parse_sql_copy_tables
from transform import transform_all
from load import load_tables

def run_etl():
    start_time = time.time()
    print("==================================================")
    print("Starting Fast and Safe ETL Pipeline")
    print("==================================================")
    
    sql_path = os.path.abspath("data/copia-BD.sql")
    output_dir = os.path.abspath("dw_data")
    
    # Tables to extract from the SQL dump
    target_tables = [
        "auth_user",
        "ciudad",
        "cliente",
        "sede",
        "departamento",
        "clientes_mensajeroaquitoy",
        "clientes_usuarioaquitoy",
        "mensajeria_servicio",
        "mensajeria_estadosservicio",
        "mensajeria_novedadesservicio",
        "mensajeria_tiponovedad",
        "mensajeria_tipovehiculo"
    ]
    
    # 1. Extraction
    print("\n--- PHASE 1: EXTRACTION ---")
    raw_dfs = parse_sql_copy_tables(sql_path, target_tables)
    
    # 2. Transformation
    print("\n--- PHASE 2: TRANSFORMATION ---")
    dw_dfs = transform_all(raw_dfs)
    
    # 3. Loading
    print("\n--- PHASE 3: LOADING ---")
    load_tables(dw_dfs, output_dir)
    
    elapsed_time = time.time() - start_time
    print("==================================================")
    print(f"ETL completed successfully in {elapsed_time:.2f} seconds!")
    print("==================================================")

if __name__ == "__main__":
    run_etl()
