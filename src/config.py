import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class Config:     
    
    target_tables = [
        "auth_user",
        "ciudad",
        "cliente",
        #"tipo_cliente",
        "sede",
        "departamento",
        "clientes_mensajeroaquitoy",
        "clientes_usuarioaquitoy",
        "mensajeria_servicio",
        #"mensajeria_tiposervicio",
        "mensajeria_estadosservicio",
        "mensajeria_novedadesservicio",
        "mensajeria_tiponovedad",
        "mensajeria_tipovehiculo"
    ]
    
    @classmethod
    def get_engine(cls):
        """
        Genera y retorna el motor de conexión a Supabase de forma dinámica.
        """

        USER = os.getenv("DB_USER")      
        PASSWORD = os.getenv("DB_PASSWORD")
        HOST = os.getenv("DB_HOST")
        PORT = os.getenv("DB_PORT", "6543") 
        DBNAME = os.getenv("DB_NAME")

        if not all([USER, PASSWORD, HOST, DBNAME]):
            raise ValueError("Error: Faltan variables de entorno en el archivo .env")

        DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
        
        return create_engine(DATABASE_URL)
