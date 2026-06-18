import os
import sys
import time

from transform.transform import transform_all
from load.load import load_tables
from extract.extract import extract_data_frames
from config import Config

def run_etl():
    """
    Ejecuta el ETL completo en sus tres fases siguiendo una estructura modular
    """
    start_time = time.time()
    
    print("==================================================")
    print("Starting Fast and Safe ETL Pipeline")
    print("==================================================")
    
    target_tables = Config.target_tables
    
    # 1. Extract
    print("\n--- PHASE 1: EXTRACTION ---")
    raw_dfs = extract_data_frames(target_tables)
    
    # 2. Transform
    print("\n--- PHASE 2: TRANSFORMATION ---")
    dw_dfs = transform_all(raw_dfs)
    
    # 3. Load
    print("\n--- PHASE 3: LOADING ---")
    load_tables(dw_dfs)
    
    elapsed_time = time.time() - start_time
    print("==================================================")
    print(f"ETL completed successfully in {elapsed_time:.2f} seconds!")
    print("==================================================")

if __name__ == "__main__":
    run_etl()
