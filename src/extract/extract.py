import pandas as pd
from config import Config
from typing import List, Dict

def extract_data_frames() -> Dict[str, pd.DataFrame]:
    
    data_frames : Dict = {}
    engine = Config.get_engine()
    
    for table_name in Config.TARGET_TABLES: 
        data_frames[table_name] = pd.read_sql(
            f"SELECT * FROM {table_name}", 
            con=engine)
        
    return data_frames