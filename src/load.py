import os
import pandas as pd

def load_tables(dfs, output_dir):
    """
    Saves the dimensional and fact DataFrames as CSV files in the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
        
    for name, df in dfs.items():
        output_path = os.path.join(output_dir, f"{name}.csv")
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"Saved {name}.csv ({len(df)} rows) to {output_path}")
        
    print("Loading phase completed successfully!")
