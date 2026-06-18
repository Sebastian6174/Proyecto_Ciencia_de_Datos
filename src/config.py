import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class Config:     
    
    PRIMARY_KEYS = {
        "dim_ciudad": "Ciudad_Key",
        "dim_cliente": "Cliente_Key",
        "dim_sede": "Sede_Key",
        "dim_mensajero": "Mensajero_Key",
        "dim_tipo_urgencia": "Tipo_Urgencia_Key",
        "dim_servicio": "Servicio_Key",
        "dim_tipo_novedad": "Tipo_Novedad_Key",
        "dim_hora": "Hora_Key",
        "dim_fecha": "Fecha_Key",
    }

    FOREIGN_KEYS = {
        "fact_servicios": {
            "Fecha_Solicitud_Key": ("dim_fecha", "Fecha_Key"),
            "Fecha_Asignacion_Key": ("dim_fecha", "Fecha_Key"),
            "Fecha_Cierre_Key": ("dim_fecha", "Fecha_Key"),
            "Hora_Solicitud_Key": ("dim_hora", "Hora_Key"),
            "Hora_Asignacion_Key": ("dim_hora", "Hora_Key"),
            "Hora_Cierre_Key": ("dim_hora", "Hora_Key"),
            "Mensajero_Key": ("dim_mensajero", "Mensajero_Key"),
            "Cliente_Key": ("dim_cliente", "Cliente_Key"),
            "Sede_Key": ("dim_sede", "Sede_Key"),
            "Ciudad_Origen_Key": ("dim_ciudad", "Ciudad_Key"),
            "Ciudad_Destino_Key": ("dim_ciudad", "Ciudad_Key"),
            "Tipo_Urgencia_Key": ("dim_tipo_urgencia", "Tipo_Urgencia_Key"),
            "Servicio_Key": ("dim_servicio", "Servicio_Key"),
        },
        "fact_novedades": {
            "Fecha_Key": ("dim_fecha", "Fecha_Key"),
            "Mensajero_Key": ("dim_mensajero", "Mensajero_Key"),
            "Tipo_Novedad_Key": ("dim_tipo_novedad", "Tipo_Novedad_Key"),
            "Servicio_Key": ("dim_servicio", "Servicio_Key"),
        },
    }
    
    TARGET_TABLES = [
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
