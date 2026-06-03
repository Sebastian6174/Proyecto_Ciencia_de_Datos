import os
import pandas as pd
import io

def parse_sql_copy_tables(sql_path, target_tables):
    """
    Parses a PostgreSQL SQL dump file to extract specific tables that use the COPY command.
    Returns a dictionary of pandas.DataFrames for the target tables.
    """
    tables_data = {table: [] for table in target_tables}
    tables_columns = {table: [] for table in target_tables}
    
    print(f"Starting extraction from {sql_path}...")
    
    current_table = None
    in_copy = False
    
    with open(sql_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("COPY public."):
                # Find if this table is in target_tables
                parts = line.split(" ")
                table_name = parts[1].split(".")[1]
                if table_name in target_tables:
                    current_table = table_name
                    in_copy = True
                    # Extract columns
                    cols_part = line.split("(")[1].split(")")[0]
                    tables_columns[current_table] = [c.strip().strip('"') for c in cols_part.split(",")]
                    print(f"Extracting table: {current_table}")
                continue
                
            if in_copy:
                stripped = line.strip("\r\n")
                if stripped == r"\.":
                    in_copy = False
                    current_table = None
                    continue
                # Split fields by tab
                row = stripped.split("\t")
                # Replace SQL NULL (\N) with None
                row = [None if val == r"\N" else val for val in row]
                tables_data[current_table].append(row)
                
    dfs = {}
    for table in target_tables:
        cols = tables_columns[table]
        data = tables_data[table]
        if cols:
            # Create DataFrame
            dfs[table] = pd.DataFrame(data, columns=cols)
            print(f"Loaded {table}: {len(dfs[table])} rows.")
        else:
            dfs[table] = pd.DataFrame()
            print(f"Warning: Table {table} not found or has no columns.")
            
    return dfs
